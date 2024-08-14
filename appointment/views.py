from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render

from patient.models import Patient

from doctor.models import Doctor

from appointment.models import AppointmentWard

from appointment.models import PatientAppointment

from common_function.date_formate import convert_date_format


# Create your views here.
def add_appointment(request):
    if request.method == 'POST':
        form = request.POST
        appoint_ward = form.get('appointment_ward')
        patient = form.get('patient_search_id')
        doctor = form.get('doctor')
        diseases = form.get('diseases')
        patient_bp_min = form.get('patient_bp_min')
        patient_bp_max = form.get('patient_bp_max')
        patient_weight = form.get('patient_weight')
        ward_fees = form.get('ward_fees')
        cash = int(form.get('cash'))
        online = int(form.get('online'))
        remaining = int(form.get('remaining'))

        appointment_date = form.get('appoint_date')
        appointment_date = convert_date_format(appointment_date)
        appointment_time = form.get('appoint_time')
        appointment_time = datetime.strptime(appointment_time, '%I:%M %p').time()
        status = 'failed!'
        msg = 'Appointment failed.'
        try:
            appoint_obj = PatientAppointment.objects.create(appoint_ward_id=appoint_ward,
                                                            doctor_id=doctor,
                                                            patient_id=patient,
                                                            patient_diseases=diseases,
                                                            patient_bp_min=patient_bp_min,
                                                            patient_bp_max=patient_bp_max,
                                                            patient_weight=patient_weight,
                                                            fees=ward_fees,
                                                            paid=cash + online,
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
        appointment_ward = AppointmentWard.objects.all()
        context = {
            'doctor': doctor,
            'appointment_ward': appointment_ward,
        }
        return render(request, 'add_appointment.html', context)


def all_appointment(request):
    appointment = PatientAppointment.objects.all()
    context = {
        'appointment': appointment,
    }
    return render(request, 'all_appointment.html', context)


def search_patient(request):
    if 'term' in request.GET:
        qs = Patient.objects.filter(patient_code__icontains=request.GET.get('term'))
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


def patient_appointment_detail(request, id):
    appointment = PatientAppointment.objects.get(id=id)
    context = {
        'appointment': appointment
    }
    return render(request, 'patient_appointment_detail.html', context)
