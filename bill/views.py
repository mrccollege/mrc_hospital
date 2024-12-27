from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from .models import PatientBill, PatientBillDetail
from store.models import Store
from django.db.models import Sum, Q

from appointment.models import PatientAppointment

from my_order.models import MedicineOrderHead, MedicineOrderDetail

from my_order.models import MedicineOrderBillHead

from my_order.models import EstimateMedicineOrderBillHead
from django.utils.timezone import localtime

from account.models import User
from patient.models import Patient


# Create your views here.
@login_required(login_url='/account/user_login/')
def bill_list(request):
    user_id = request.session['user_id']
    query = Q()
    try:
        store = Store.objects.get(user_id=user_id)
        store_id = store.id
        query = Q(store_id=store_id)
    except:
        pass
    patient = PatientBill.objects.filter(query)
    context = {
        'patient': patient,
    }
    return render(request, 'bill_list.html', context)


def patient_bill_detail(request, id):
    patient_details = PatientBill.objects.get(id=id)
    bill_details = PatientBillDetail.objects.filter(patient_bill_id=id)
    total_sell_price = bill_details.aggregate(Sum('medicine_sell_price'))['medicine_sell_price__sum'] or 0
    context = {
        'patient_details': patient_details,
        'bill_details': bill_details,
        'total_sell_price': total_sell_price,
    }
    return render(request, 'patient_bill_detail.html', context)


def appointment_patient_bill_detail(request, id):
    appointment = PatientAppointment.objects.get(id=id)
    context = {
        'appointment_id': id,
        'appointment': appointment,
    }
    return render(request, 'appointment_patient_bill.html', context)


def order_list(request):
    order = MedicineOrderHead.objects.filter(status=0)
    context = {
        'order': order
    }
    return render(request, 'order_list.html', context)


def normal_order_bill_list(request):
    order = MedicineOrderBillHead.objects.all().order_by('-created_at__date')
    context = {
        'order': order
    }
    return render(request, 'normal_order_bill_list.html', context)


def estimate_order_bill_list(request):
    order = EstimateMedicineOrderBillHead.objects.filter(status=1)
    context = {
        'order': order
    }
    return render(request, 'estimate_order_bill_list.html', context)


def order_detail(request, id):
    user = MedicineOrderHead.objects.get(id=id)
    medicine = MedicineOrderDetail.objects.filter(head_id=id)
    context = {
        'id': id,
        'user': user,
        'medicine': medicine,
    }
    return render(request, 'order_detail.html', context)


def create_customer_bill(request, order_type=0):
    if request.method == 'POST':
        form = request.POST
        username = form.get('name')
        mobile = form.get('mobile')
        email = form.get('email')
        patient_age = form.get('age')
        sex = form.get('gender')

        patient_code = datetime.now().strftime("%Y%d%H%M%S")
        status = 'failed'
        msg = 'Patient Registration failed.'
        try:
            user_obj = User.objects.create_user(username=username.title(),
                                                email=email,
                                                password='12345',
                                                mobile=mobile,
                                                sex=sex,
                                                age=patient_age,
                                                )
            if user_obj:
                patient_id = user_obj.id
                Patient.objects.create(user_id=patient_id,
                                       patient_code=patient_code,
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

    context = {
        'order_type': order_type,
    }
    if order_type == 1:
        return render(request, 'customer_bill/create_customer_bill_instate.html', context)
    elif order_type == 2:
        return render(request, 'customer_bill/create_customer_bill_other_state.html', context)
    elif order_type == 3:
        return render(request, 'customer_bill/create_customer_bill_of_supply.html', context)
    else:
        return render(request, 'customer_bill/create_customer_bill.html', context)

