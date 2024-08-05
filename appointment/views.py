from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render

from patient.models import Patient

from doctor.models import Doctor


# Create your views here.
def add_appointment(request):
    doctor = Doctor.objects.all()
    context = {
        'doctor': doctor
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
