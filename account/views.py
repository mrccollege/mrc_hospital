from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .models import User
from hospital_detail.models import Hospital

from store.models import Store

from doctor.models import Doctor

from patient.models import Patient


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
        address = form.get('address')
        status = 'failed'
        msg = 'Registration failed.'
        try:
            user_obj = User.objects.create_user(username=store_name,
                                                email=email,
                                                password=password,
                                                mobile=mobile,
                                                phone=phone,
                                                address=address)
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
        address = form.get('address')
        specialist = form.get('specialist')
        degree = form.get('degree')
        status = 'failed'
        msg = 'Doctor Registration failed.'
        try:
            user_obj = User.objects.create_user(username=username,
                                                email=email,
                                                password='12345',
                                                mobile=mobile,
                                                phone=phone,
                                                address=address)
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
    return render(request, 'doctor_registration.html')


def patient_registration(request):
    if request.method == 'POST':
        # User.objects.filter(username='rajat').delete()
        form = request.POST
        username = form.get('patient_name')
        mobile = form.get('mobile')
        email = mobile + '@yopmail.com'
        phone = form.get('phone')
        address = form.get('address')
        patient_age = form.get('patient_age')
        patient_code = datetime.now().strftime("%Y%d%H%M%S")
        status = 'failed'
        msg = 'Patient Registration failed.'
        try:
            user_obj = User.objects.create_user(username=username,
                                                email=email,
                                                password='12345',
                                                mobile=mobile,
                                                phone=phone,
                                                address=address)
            if user_obj:
                patient_id = user_obj.id
                Patient.objects.create(user_id=patient_id,
                                       patient_code=patient_code,
                                       patient_age=patient_age,
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
    return render(request, 'patient_registration.html')


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



