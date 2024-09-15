from diagnosis.models import DiagnosisPosition, DiagnosisType
from django.http import JsonResponse


# Create your views here.
def get_diagnosis_position(request):
    if request.method == 'GET':
        form = request.GET
        name_id = form.get('name_id')
        position = DiagnosisPosition.objects.filter(name_id=name_id).values('id', 'position')
        position = list(position)
        context = {
            'position': position,
        }
        return JsonResponse(context)


def get_diagnosis_type(request):
    if request.method == 'GET':
        form = request.GET
        position_id = form.get('position_id')
        type = DiagnosisType.objects.filter(position_id=position_id).values('id', 'type')
        type = list(type)
        context = {
            'type': type,
        }
        return JsonResponse(context)
