from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .models import User
from hospital_detail.models import Hospital

from store.models import Store

from doctor.models import Doctor

from patient.models import Patient, OtherReference

from address_place.models import Country

from patient.models import SocialMediaReference


# Create your views here.
def hospital_registration(request):
    if request.method == 'POST':
        form = request.POST
        hospital_name = form.get('hospital_name')
        email = form.get('email')
        mobile = form.get('mobile')
        phone = form.get('phone')
        address = form.get('address')
        status = 'failed'
        msg = 'Registration failed.'
        try:
            user_obj = User.objects.create_user(username=hospital_name,
                                                email=email,
                                                password='12345678',
                                                mobile=mobile,
                                                phone=phone,
                                                address=address)
            if user_obj:
                hospital_id = user_obj.id
                Hospital.objects.create(user_id=hospital_id)
                status = 'success'
                msg = 'Registration successfully.'

        except Exception as e:
            status = status
            msg = str(e)

        context = {
            'status': status,
            'msg': msg,
        }
        return JsonResponse(context)
    return render(request, 'hospital_registration.html')


def store_registration(request):
    if request.method == 'POST':
        form = request.POST
        store_name = form.get('store_name')
        mobile = form.get('mobile')
        email = mobile + '@yopmail.com'
        password = form.get('password')
        phone = form.get('phone')
        status = 'failed'
        msg = 'Registration failed.'
        try:
            user_obj = User.objects.create_user(username=store_name.title(),
                                                email=email,
                                                password=password,
                                                mobile=mobile,
                                                phone=phone,)
            if user_obj:
                store_id = user_obj.id
                is_main_store = Store.objects.filter(type='MAIN')
                if is_main_store:
                    type = 'MINI'
                else:
                    type = 'MAIN'
                Store.objects.create(user_id=store_id, type=type)
                status = 'success'
                msg = 'Registration successfully.'

        except Exception as e:
            status = status
            msg = str(e)

        context = {
            'status': status,
            'msg': msg,
        }
        return JsonResponse(context)
    return render(request, 'store_registration.html')


def doctor_registration(request):
    if request.method == 'POST':
        form = request.POST
        username = form.get('doctor_name')
        mobile = form.get('mobile')
        email = mobile + '@yopmail.com'
        phone = form.get('phone')

        house_flat = form.get('house_flat')
        street = form.get('street')
        city = form.get('city')
        district = form.get('district')
        pincode = form.get('pincode')
        country = form.get('country')
        state = form.get('state')

        specialist = form.get('specialist')
        degree = form.get('degree')
        status = 'failed'
        msg = 'Doctor Registration failed.'
        try:
            user_obj = User.objects.create_user(username=username.title(),
                                                email=email,
                                                password='12345',
                                                mobile=mobile,
                                                phone=phone,
                                                house_flat=house_flat,
                                                street_colony=street,
                                                city=city,
                                                district=district,
                                                pin=pincode,
                                                state_id=state,
                                                country_id=country,
                                                )
            if user_obj:
                doctor_id = user_obj.id
                Doctor.objects.create(user_id=doctor_id,
                                      specialist=specialist.upper(),
                                      degree=degree.upper()
                                      )
                status = 'success'
                msg = 'Doctor Registration successfully.'

        except Exception as e:
            status = status
            msg = str(e)

        context = {
            'status': status,
            'msg': msg,
        }
        return JsonResponse(context)
    else:
        country = Country.objects.all()
        context = {
            'country': country,
        }
        return render(request, 'doctor_registration.html', context)


def patient_registration(request):
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
        email = mobile + '@yopmail.com'
        phone = form.get('phone')

        patient_code = datetime.now().strftime("%Y%d%H%M%S")
        status = 'failed'
        msg = 'Patient Registration failed.'
        try:
            user_obj = User.objects.create_user(username=username.title(),
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
                    social_media = None
                if reference_by_other:
                    reference_by_other = None
                if reference_by_patient:
                    reference_by_patient = None
                patient_id = user_obj.id
                Patient.objects.create(user_id=patient_id,
                                       patient_code=patient_code,
                                       social_media_id=social_media,
                                       other_reference_id=reference_by_other,
                                       reference_by_patient_id=reference_by_patient,
                                       )
                status = 'success'
                msg = 'Patient Registration successfully.'

        except Exception as e:
            status = status
            msg = str(e)

        context = {
            'status': status,
            'msg': msg,
        }
        return JsonResponse(context)
    else:
        country = Country.objects.all()
        social_media = SocialMediaReference.objects.all()
        reference_by_other = OtherReference.objects.all()
        context = {
            'country': country,
            'social_media': social_media,
            'reference_by_other': reference_by_other
        }
        return render(request, 'patient_registration.html', context)


def user_login(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        status = 'failed'
        msg = 'Account does not exist for this number, please enter the correct mobile number.'

        try:
            user = User.objects.get(mobile__iexact=mobile)
            user_name = user.username
            user = authenticate(username=user_name, password=password)
            if user is not None:
                login(request, user)
                request.session['user_id'] = user.id
                status = 'success'
                msg = 'Login successful.'
            else:
                msg = 'Invalid password.'
        except User.DoesNotExist:
            msg = msg
        except Exception as e:
            msg = str(e)

        context = {
            'status': status,
            'msg': msg,
        }
        return JsonResponse(context)
    return render(request, 'user_login.html')


def user_logout(request):
    logout(request)
    request.session.flush()
    return redirect('/account/user_login/')


def update_user_detail(request):
    if request.method == 'POST':
        form = request.POST
        user_id = form.get('user_id')
        mobile = form.get('mobile')
        house_flat = form.get('house_flat')
        street_colony = form.get('street_colony')
        city = form.get('city')
        district = form.get('district')
        pin = form.get('pin')
        state = form.get('state')
        country = form.get('country')
        User.objects.filter(id=user_id).update(mobile=mobile,
                                               house_flat=house_flat,
                                               street_colony=street_colony,
                                               city=city,
                                               district=district,
                                               pin=pin,
                                               # state=state,
                                               # country=country,
                                               )
        status = 'success'
        msg = 'Information has been updated.'
        context = {
            'status': status,
            'msg': msg,
        }
        return JsonResponse(context)
