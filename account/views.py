from django.http import JsonResponse
from django.shortcuts import render

from .models import User
from hospital_detail.models import Hospital

from store.models import Store


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
        email = form.get('email')
        mobile = form.get('mobile')
        phone = form.get('phone')
        address = form.get('address')
        status = 'failed'
        msg = 'Registration failed.'
        try:
            user_obj = User.objects.create_user(username=store_name,
                                                email=email,
                                                password='12345678',
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
