from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from .models import MainStoreMedicine, Store, MainStoreMedicineTransaction, MainToMiniStoreMedicine, \
    MainToMiniStoreMedicineTransaction


# Create your views here.
def main_store(request):
    store = MainStoreMedicine.objects.all()
    store_name = store[0].store
    context = {
        'store_name': store_name,
        'store': store
    }
    return render(request, 'main_store_detail.html', context)


def transfer_medicine_detail(request, id):
    store_medicine = MainStoreMedicine.objects.get(id=id)
    store_name = store_medicine.store

    mini_store = Store.objects.filter(type='MINI')
    context = {
        'store_name': store_name,
        'store_medicine': store_medicine,
        'mini_store': mini_store
    }
    return render(request, 'transfer_medicine_from_main_store.html', context)


def transfer_medicine_from_main(request):
    if request.method == 'POST':
        form = request.POST
        medicine_id = int(form.get('medicine_id'))
        mini_store_id = int(form.get('mini_store_id'))
        transfer_medicine_qty = int(form.get('transfer_medicine_qty'))
        medicine = MainStoreMedicine.objects.get(medicine_id=medicine_id)
        store_id = medicine.store.id
        existing_qty = medicine.qty
        if existing_qty >= transfer_medicine_qty:
            medicine_qty = existing_qty - transfer_medicine_qty
        else:
            status = 'failed'
            context = {
                'status': status
            }
            return JsonResponse(context)
        query = Q(medicine_id=medicine_id, from_store_id=store_id, to_store_id=mini_store_id)
        is_medicine = MainToMiniStoreMedicine.objects.filter(query)
        if is_medicine:
            pre_qty = is_medicine[0].qty
            obj = MainToMiniStoreMedicine.objects.filter(query).update(qty=transfer_medicine_qty)
        else:
            obj = MainToMiniStoreMedicine.objects.create(from_store_id=store_id,
                                                         to_store_id=mini_store_id,
                                                         medicine_id=medicine_id,
                                                         qty=transfer_medicine_qty,
                                                         )
            obj_id = obj.id
        if obj:
            MainStoreMedicine.objects.filter(medicine_id=medicine_id).update(qty=medicine_qty)
            MainToMiniStoreMedicineTransaction.objects.create()
            status = 'success'
        else:
            MainToMiniStoreMedicine.objects.filter(query).update(qty=pre_qty)
            MainToMiniStoreMedicine.objects.filter(id=obj_id).delete()
            status = 'failed'

        context = {
            'status': status
        }
        return JsonResponse(context)


def medicine_add_transaction_history(request):
    transaction = MainStoreMedicineTransaction.objects.all()
    store_name = transaction[0].store
    context = {
        'store_name': store_name,
        'transaction': transaction,
    }
    return render(request, 'medicine_add_transaction_history.html', context)


def mini_store(request):
    store = Store.objects.filter(type='MINI').order_by('-id')
    context = {
        'store': store
    }
    return render(request, 'mini_store_detail.html', context)


def view_mini_store_medicine(request, id):
    store_medicine = MainToMiniStoreMedicine.objects.filter(to_store_id=id)
    context = {
        'store_medicine': store_medicine
    }
    return render(request, 'mini_store_medicine_detail.html', context)
