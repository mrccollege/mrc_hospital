from django.http import JsonResponse
from django.shortcuts import render

from patient.models import Patient, OtherReference

from account.models import User


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
        mobile = form.get('mobile')
        email = mobile + 'yopmail.com'
        password = form.get('password')
        phone = form.get('phone')
        address = form.get('address')
        patient_diseases = form.get('diseases')
        patient_bp_min = form.get('patient_bp_min')
        patient_bp_max = form.get('patient_bp_max')
        patient_weight = form.get('patient_weight')
        patient_age = form.get('patient_age')
        status = 'failed'
        msg = 'Patient Detail Updated failed.'
        try:
            patient_obj = Patient.objects.filter(id=id).update(patient_diseases=patient_diseases,
                                                               patient_bp_min=patient_bp_min,
                                                               patient_bp_max=patient_bp_max,
                                                               patient_weight=patient_weight,
                                                               patient_age=patient_age
                                                               )
            if patient_obj:
                user_id = Patient.objects.get(id=id)
                user_id = user_id.user.id
                user_obj = User.objects.filter(id=user_id).update(username=username,
                                                                  email=email,
                                                                  mobile=mobile,
                                                                  phone=phone,
                                                                  address=address)
                if user_obj:
                    if password:
                        u = Patient.objects.get(id=id)
                        u.set_password(password)
                        u.save()

                status = 'success'
                msg = 'Patient Detail Updated successfully.'

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
        context = {
            'id': id,
            'patient': patient
        }
        return render(request, 'patient_detail.html', context)


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
