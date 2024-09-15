from datetime import datetime

from django.db.models import Q, Case, When
from django.http import JsonResponse
from django.shortcuts import render

from patient.models import Patient, OtherReference, SocialMediaReference
from account.models import User
from address_place.models import Country


# Create your views here.
def patient_list(request):
    patient = Patient.objects.all()
    context = {
        'patient': patient
    }
    return render(request, 'patient_list.html', context)


def patient_detail(request, id):
    if request.method == 'POST':
        form = request.POST
        username = form.get('patient_name')
        care_of = form.get('care_of')
        mobile = form.get('mobile')
        patient_age = form.get('patient_age')
        sex = form.get('sex')
        house_flat = form.get('house_flat')
        street = form.get('street')
        city = form.get('city')
        district = form.get('district')
        pincode = form.get('pincode')
        country = form.get('country')
        state = form.get('state')
        reference_by_patient = form.get('patient_search_id')
        reference_by_other = form.get('reference_by_other')
        social_media = form.get('social_media')
        print(social_media, '============social_media=====')
        email = mobile + '@yopmail.com'
        phone = form.get('phone')
        status = 'failed'
        msg = 'Patient Registration failed.'
        try:
            user = Patient.objects.get(id=id)
            user_obj = User.objects.filter(id=user.user.id).update(username=username.title(),
                                                                   email=email,
                                                                   password='12345',
                                                                   mobile=mobile,
                                                                   phone=phone,
                                                                   care_of=care_of.title(),
                                                                   sex=sex,
                                                                   age=patient_age,
                                                                   house_flat=house_flat,
                                                                   street_colony=street,
                                                                   city=city,
                                                                   district=district,
                                                                   pin=pincode,
                                                                   state_id=state,
                                                                   country_id=country,
                                                                   )
            if user_obj:
                if social_media:
                    social_media = social_media
                else:
                    social_media = None
                if reference_by_other:
                    reference_by_other = reference_by_other
                else:
                    reference_by_other = None
                if reference_by_patient:
                    reference_by_patient = reference_by_patient
                else:
                    reference_by_patient = None
                Patient.objects.filter(id=id).update(social_media_id=social_media,
                                                     other_reference_id=reference_by_other,
                                                     reference_by_patient_id=reference_by_patient,
                                                     )
                status = 'success'
                msg = 'Patient updated successfully.'

        except Exception as e:
            status = status
            msg = str(e)

        context = {
            'status': status,
            'msg': msg,
        }
        return JsonResponse(context)
    else:
        patient = Patient.objects.get(id=id)
        country = Country.objects.annotate(
            is_patient_country=Case(
                When(id=patient.user.country.id, then=0),
                default=1,
            )
        ).order_by('is_patient_country', 'name')

        if patient.social_media:
            reference_social_media_id = patient.social_media.id
        else:
            reference_social_media_id = None
        social_media = SocialMediaReference.objects.annotate(
            is_social_media=Case(
                When(id=reference_social_media_id, then=0),
                default=1,)
        ).order_by('is_social_media', 'title')
        if patient.reference_by_patient:
            reference_by_patient_id = patient.reference_by_patient.id
        else:
            reference_by_patient_id = None
        reference_by_other = OtherReference.objects.annotate(
            is_reference_by_other=Case(
                When(id=reference_by_patient_id, then=0),
                default=1,
            )
        ).order_by('is_reference_by_other', 'name')
        context = {
            'country': country,
            'social_media': social_media,
            'reference_by_other': reference_by_other,
            'id': id,
            'patient': patient
        }
        return render(request, 'patient_detail.html', context)


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


def add_other_reference(request):
    if request.method == 'POST':
        form = request.POST
        reference_name = form.get('reference_name')
        reference_mobile = form.get('reference_mobile')
        reference_address = form.get('reference_address')
        patient_obj = OtherReference.objects.create(name=reference_name,
                                                    mobile=reference_mobile,
                                                    address=reference_address, )
        patient_dict = {
            'id': patient_obj.id,
            'name': patient_obj.name,
            'mobile': patient_obj.mobile,
        }
        if patient_obj:
            patient_obj = patient_dict
            status = 'success'
            msg = 'Reference registered successfully.'
        else:
            patient_obj = {}
            status = 'failed'
            msg = 'Reference registered failed.'

        context = {
            'status': status,
            'msg': msg,
            'patient_obj': patient_obj,
        }
        return JsonResponse(context)
