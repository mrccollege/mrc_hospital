from address_place.models import State
from django.db.models import Case, When
from django.http import JsonResponse

from patient.models import Patient


def get_state(request):
    if request.method == 'GET':
        country_id = request.GET.get('country_id')
        patient_id = request.GET.get('patient_id')
        if country_id and patient_id is not None:
            patient = Patient.objects.get(id=patient_id)
            user_state_id = patient.user.state.id
            states = State.objects.filter(country_id=country_id).annotate(
                is_patient_state=Case(
                    When(id=user_state_id, then=0),  # Assign 0 if it's the patient's state
                    default=1,  # Assign 1 to all other states
                )
            ).order_by('is_patient_state', 'name').values('id', 'name')
        else:
            states = State.objects.filter(country_id=country_id).values('id', 'name')

        state_list = list(states)
        context = {
            'status': 'success',
            'state': state_list,
        }
        return JsonResponse(context)
