from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render

from patient.models import Patient


# Create your views here.
def add_appointment(request):
    return render(request, 'add_appointment.html')


def search_patient(request):
    if 'term' in request.GET:
        # print(request.GET.get('term'), '===============@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        qs = Patient.objects.filter(patient_code__icontains=request.GET.get('term'))
        suggestions = list(qs.values_list('user__username', flat=True))
        print(suggestions, '======================suggestions================')
        return JsonResponse(suggestions, safe=False)
    return JsonResponse([], safe=False)
