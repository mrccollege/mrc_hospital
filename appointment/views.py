from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from patient.models import Patient

from doctor.models import Doctor

from appointment.models import AppointmentWard

from appointment.models import PatientAppointment

from common_function.date_formate import convert_date_format

from account.models import User


# Create your views here.
def add_appointment(request):
    if request.method == 'POST':
        form = request.POST
        appointment_slot = form.get('appointment_slot')
        patient_search_id = form.get('patient_search_id')
        doctor_id = form.get('doctor_id')
        diseases = form.get('diseases')
        patient_bp = form.get('patient_bp')
        pulse = form.get('pulse')
        oxygen = form.get('oxygen')
        temperature = form.get('temperature')
        respiration = form.get('respiration')
        weight = form.get('weight')
        extra_fees = form.get('extra_fees')
        ward_fees = form.get('ward_fees')
        cash = int(form.get('cash'))
        online = int(form.get('online'))
        remaining = int(form.get('remaining'))
        discount = int(form.get('discount'))
        appointment_date = form.get('appoint_date')
        appointment_date = convert_date_format(appointment_date)
        appointment_time = form.get('appoint_time')
        appointment_time = datetime.strptime(appointment_time, '%I:%M %p').time()
        status = 'failed!'
        msg = 'Appointment failed.'
        try:
            appoint_obj = PatientAppointment.objects.create(appoint_ward_id=appointment_slot,
                                                            doctor_id=doctor_id,
                                                            patient_id=patient_search_id,
                                                            patient_diseases=diseases,
                                                            patient_bp=patient_bp,
                                                            pulse=pulse,
                                                            oxygen=oxygen,
                                                            temperature=temperature,
                                                            respiration=respiration,
                                                            patient_weight=weight,
                                                            extra_fees=extra_fees,
                                                            discount=discount,
                                                            fees=ward_fees,
                                                            pay_amount=cash + online,
                                                            remaining=remaining,
                                                            cash=cash,
                                                            online=online,
                                                            appointment_date=appointment_date,
                                                            appointment_time=appointment_time,
                                                            )
            if appoint_obj:
                status = 'success'
                msg = 'Appointment successfully saved.'

        except Exception as e:
            msg = str(e)

        context = {
            'status': status,
            'msg': msg,
        }
        return JsonResponse(context)
    else:
        doctor = Doctor.objects.all()
        appointment_slot = AppointmentWard.objects.all()
        context = {
            'doctor': doctor,
            'appointment_slot': appointment_slot,
        }
        return render(request, 'add_appointment.html', context)


@login_required(login_url='/account/user_login/')
def all_appointment(request):
    user_id = request.session.get('user_id')
    is_admin = User.objects.get(id=user_id)
    if is_admin.user_type == 'ADMIN':
        query = Q()
    else:
        query = Q(doctor__user__id=user_id, appoint_status='unchecked')
        # query = Q(doctor__user__id=user_id, appoint_status='checked')
    appointment = PatientAppointment.objects.filter(query)
    context = {
        'appointment': appointment,
    }
    return render(request, 'all_appointment.html', context)


def search_patient(request):
    if 'term' in request.GET:
        search_value = request.GET.get('term')
        if search_value:
            search_terms = search_value.split()
            for term in search_terms:
                query = Q(user__username__icontains=term) | Q(patient_code__icontains=term)
                qs = Patient.objects.filter(query)
                data_list = []
                for i in qs:
                    data_dict = {}
                    data_dict['id'] = i.id
                    data_dict['name'] = i.user.username
                    data_dict['code'] = i.patient_code
                    data_list.append(data_dict)
                context = {
                    'data_list': data_list
                }
                return JsonResponse(context, safe=False)
            return JsonResponse([], safe=False)


@login_required(login_url='/account/user_login/')
def patient_appointment_detail(request, id):
    appointment = PatientAppointment.objects.get(id=id)
    context = {
        'appointment_id': id,
        'appointment': appointment
    }
    return render(request, 'patient_appointment_detail.html', context)
