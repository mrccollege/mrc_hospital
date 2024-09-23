from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import PatientBill, PatientBillDetail
from store.models import Store
from django.db.models import Sum, Q

from appointment.models import PatientAppointment

from my_order.models import MedicineOrderHead, MedicineOrderDetail


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


def order_received(request, id):
    user = MedicineOrderHead.objects.get(id=id)
    medicine = MedicineOrderDetail.objects.filter(head_id=id)
    context = {
        'id': id,
        'user': user,
        'medicine': medicine,
    }
    return render(request, 'order_received.html', context)
