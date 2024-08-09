from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import PatientBill, PatientBillDetail
from store.models import Store
from django.db.models import Sum

# Create your views here.
@login_required(login_url='/account/user_login/')
def bill_list(request):
    user_id = request.session['user_id']
    store = Store.objects.get(user_id=user_id)
    store_id = store.id
    patient = PatientBill.objects.filter()
    context = {
        'patient': patient,
    }
    return render(request, 'bill_list.html', context)


def patient_bill_detail(request, id):
    bill_details = PatientBillDetail.objects.filter(patient_bill_id=id)
    total_sell_price = bill_details.aggregate(Sum('medicine_sell_price'))['medicine_sell_price__sum'] or 0
    print(total_sell_price, '======total_sell_price')
    context = {
        'bill_details': bill_details,
        'total_sell_price': total_sell_price,
    }
    return render(request, 'patient_bill_detail.html', context)