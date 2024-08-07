from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render

from patient.models import Patient

from doctor.models import Doctor

from appointment.models import AppointmentWard

from appointment.models import PatientAppointment


# Create your views here.
def add_appointment(request):
    if request.method == 'POST':
        form = request.POST
        appoint_ward = form.get('appointment_ward')
        patient = form.get('patient')
        doctor = form.get('doctor')
        diseases = form.get('diseases')
        patient_bp_min = form.get('patient_bp_min')
        patient_bp_max = form.get('patient_bp_max')
        patient_weight = form.get('patient_weight')
        ward_fees = form.get('ward_fees')
        cash = int(form.get('cash'))
        online = int(form.get('online'))
        remaining = int(form.get('remaining'))

        PatientAppointment.objects.filter(appoint_ward=appoint_ward,
                                          doctor=doctor,
                                          patient=patient,
                                          patient_diseases=diseases,
                                          patient_bp_min=patient_bp_min,
                                          patient_bp_max=patient_bp_max,
                                          patient_weight=patient_weight,
                                          fees=ward_fees,
                                          paid=cash+online,
                                          remaining=remaining,
                                          cash=cash,
                                          online=online,
                                          appointment_date=appointment_date,
                                          appointment_time=appointment_time,
                                          appoint_status=appoint_status,)

        context = {}
        return JsonResponse(context)
    else:
        doctor = Doctor.objects.all()
        appointment_ward = AppointmentWard.objects.all()
        context = {
            'doctor': doctor,
            'appointment_ward': appointment_ward,
        }
        return render(request, 'add_appointment.html', context)


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
