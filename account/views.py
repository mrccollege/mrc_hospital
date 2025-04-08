import time
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .models import User, OtpVerify
from hospital_detail.models import Hospital

from store.models import Store

from doctor.models import Doctor

from patient.models import Patient, OtherReference

from address_place.models import Country
import requests
from patient.models import SocialMediaReference
from django.core.mail import send_mail
from common_function.send_message import send_sms

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
        mobile = mobile[-10:]
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
                                                phone=phone, )
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
        mobile = mobile[-10:]
        email = form.get('email')
        password = form.get('password')
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

        existing_user = User.objects.filter(Q(email__iexact=email) | Q(mobile__iexact=mobile)).first()

        if existing_user:
            if existing_user.email == email and existing_user.mobile == mobile:
                msg = "This email and mobile number are already registered."
            elif existing_user.email == email:
                msg = "This email is already registered."
            elif existing_user.mobile == mobile:
                msg = "This mobile number is already registered."
            return JsonResponse({'success': False, 'msg': msg})

        try:
            user_obj = User.objects.create_user(username=username.title(),
                                                email=email,
                                                password=password,
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
        patient_name = form.get('patient_name')
        care_of = form.get('care_of')
        mobile = form.get('mobile')
        mobile = mobile[-10:]
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
        patient_id = 0

        message = f'Namaste!! Welcome to MRC Ayurveda, Access your more Details www.MrcAyurveda.com Using User ID {mobile} Password{12345}'
        # base_url = f'http://msg.msgclub.net/rest/services/sendSMS/sendGroupSms?AUTH_KEY=3380567192fd2e6d18f63985aace&message={message}&senderId=MRCARC&routeId=1&mobileNos={mobile}&smsContentType=english'
        try:
            user_obj = User.objects.create_user(username=mobile,
                                                first_name=patient_name,
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
                patient_obj = Patient.objects.create(user_id=patient_id,
                                                     patient_code=patient_code,
                                                     social_media_id=social_media,
                                                     other_reference_id=reference_by_other,
                                                     reference_by_patient_id=reference_by_patient,
                                                     )
                if patient_obj:
                    try:
                        send_sms(mobile, message)
                    except:
                        pass
                    patient_id = patient_obj.id
                    status = 'success'
                    msg = 'Patient Registration successfully.'

        except Exception as e:
            status = status
            msg = str(e)
            patient_id = 0

        context = {
            'status': status,
            'msg': msg,
            'patient_id': patient_id,
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
        mobile = mobile[-10:]
        password = request.POST.get('password')
        status = 'failed'
        msg = 'Account does not exist for this number, please enter the correct mobile number.'

        try:
            user = User.objects.filter(mobile__iexact=mobile)
            user_name = user[0].username
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


def generate_time_based_otp():
    # Get the current time in seconds
    current_time = int(time.time())
    # Convert the current time to a string and use a portion of it as the OTP
    otp = str(current_time)[-6:]

    return otp


def send_otp_email(email, otp):
    subject = 'Your OTP for Verification'
    message = f'Your OTP is: {otp}'
    from_email = 'sanjay.singh@crebritech.com'
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)


def forget_password(request):
    if request.method == 'POST':
        form = request.POST
        email = form.get('email')
        is_user = User.objects.filter(email__exact=email)
        if is_user:
            otp = generate_time_based_otp()
            otp_obj = OtpVerify.objects.filter(email__exact=email)
            if otp_obj:
                OtpVerify.objects.filter(email__exact=email).update(otp=otp)
                send_otp_email(email, otp)
                status = 1
                msg = f'OTP Send successfully on {email}'
            else:
                try:
                    OtpVerify.objects.create(email=email, otp=otp)
                    send_otp_email(email, otp)
                    status = 1
                    msg = f'OTP Send successfully on {email}'
                except Exception as e:
                    status = 0
                    msg = str(e)
        else:
            status = 0
            msg = 'Email is not registered'

        context = {
            'status': status,
            'msg': msg,
            'email': email,
        }
        return JsonResponse(context)
    else:
        return render(request, 'forget_password.html')


def verity_otp(request, email=None):
    if request.method == 'POST':
        form = request.POST
        email = form.get('email')
        otp = form.get('otp')
        new_password = form.get('new_password')
        status = 0
        msg = 'Password not reset'
        is_user = User.objects.filter(email__iexact=email)
        if is_user:
            otp_obj = OtpVerify.objects.filter(email__iexact=email, otp__iexact=otp)
            if otp_obj:
                users = User.objects.filter(email__iexact=email)
                user = users[0]
                user.set_password(new_password)
                user.save()
                status = 1
                msg = 'Password successfully reset'
                OtpVerify.objects.filter(email__iexact=email).delete()
            else:
                status = 0
                msg = msg

        context = {
            'status': status,
            'msg': msg,
            'email': email,
        }
        return JsonResponse(context)

    context = {
        'email': email
    }
    return render(request, 'verity_otp.html', context)


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
