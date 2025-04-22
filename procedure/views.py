from django.shortcuts import render
from .models import Procedure
from django.http import JsonResponse
from django.db.models import Q

from patient.models import Patient


# Create your views here.
def patient_procedure(request):
    return render(request, 'patient_procedure_data.html')


def create_procedure(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    context = {
        'patient_id': patient_id,
        'patient': patient,
    }
    return render(request, 'create_procedure.html', context)


def procedure_list(request):
    return render(request, 'procedure_list.html')


def get_procedure(request):
    if request.method == 'GET':
        form = request.GET
        search_value = form.get('search_value', '').strip()
        procedure_ids = form.getlist('procedure_ids[]')
        query = ~Q(id__in=procedure_ids)
        if search_value:
            search_terms = search_value.split()
            for term in search_terms:
                query &= Q(name__icontains=term)

        medicines = Procedure.objects.filter(query).values('id', 'name', 'price')
        data_list = [
            {
                'id': i['id'],
                'name': i['name'].capitalize(),
                'mrp': i['price'],
            }
            for i in medicines
        ]
        context = {'results': data_list}
        return JsonResponse(context)
