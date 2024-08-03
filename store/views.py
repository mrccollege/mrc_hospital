from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from .models import Store, MedicineStore, \
    MedicineStoreTransactionHistory
from medicine.models import Medicine


# Create your views here.
def main_store(request):
    store = Store.objects.filter(type='MAIN')
    if store:
        main_store_id = store[0].id
        store_name = store[0].user.username
        medicine = MedicineStore.objects.filter(to_store_id=main_store_id)
    else:
        medicine = []
        store_name = 'Please create main store.'

    context = {
        'store_name': store_name,
        'medicine': medicine
    }
    return render(request, 'main_store_detail.html', context)


def transfer_new_main_store_medicine_detail(request, id):
    store_medicine = MedicineStore.objects.get(id=id)
    store_name = store_medicine.to_store.user.username

    mini_store = Store.objects.filter(type='MINI')
    print(mini_store, '=============mini_store')
    context = {
        'recorde_id': id,
        'store_name': store_name,
        'store_medicine': store_medicine,
        'mini_store': mini_store
    }
    return render(request, 'transfer_medicine_from_main_store.html', context)


def transfer_mini_store_medicine_detail(request, record_id):
    store_medicine = MedicineStore.objects.get(id=record_id)
    from_store_id = store_medicine.to_store.id
    store_name = store_medicine.to_store.user.username

    mini_store = Store.objects.all().exclude(id=from_store_id)
    context = {
        'recorde_id': record_id,
        'from_store_id': from_store_id,
        'store_name': store_name,
        'store_medicine': store_medicine,
        'mini_store': mini_store
    }
    return render(request, 'transfer_medicine_from_mini_store.html', context)


def transfer_new_medicine_from_main(request, id):
    if request.method == 'POST':
        form = request.POST
        medicine_id = int(form.get('medicine_id'))
        to_store_id = int(form.get('to_store_id'))
        medicine_name = form.get('medicine_name')
        transfer_medicine_qty = int(form.get('transfer_medicine_qty'))
        medicine = MedicineStore.objects.get(id=id)
        main_store_id = medicine.to_store.id
        existing_qty = medicine.qty
        if existing_qty >= transfer_medicine_qty:
            medicine_qty = existing_qty - transfer_medicine_qty
        else:
            status = 'failed'
            context = {
                'status': status
            }
            return JsonResponse(context)
        query = Q(medicine_id=medicine_id, to_store_id=to_store_id)
        is_medicine = MedicineStore.objects.filter(query)
        if is_medicine:
            pre_qty = is_medicine[0].qty
            total_transfer_qty = pre_qty + transfer_medicine_qty
            obj = MedicineStore.objects.filter(query).update(qty=total_transfer_qty)
        else:
            obj = MedicineStore.objects.create(from_store_id=main_store_id,
                                               to_store_id=to_store_id,
                                               medicine_id=medicine_id,
                                               qty=transfer_medicine_qty,
                                               )
            obj_id = obj.id

        if obj:
            MedicineStore.objects.filter(medicine_id=medicine_id, to_store_id=main_store_id).update(qty=medicine_qty)
            medicine_obj = Medicine.objects.get(id=medicine_id)
            MedicineStoreTransactionHistory.objects.create(from_store_id=main_store_id,
                                                           to_store_id=to_store_id,
                                                           medicine_id=medicine_id,
                                                           medicine_name=medicine_name,
                                                           qty=transfer_medicine_qty,
                                                           medicine_manufacturer=medicine_obj.medicine_manufacturer,
                                                           medicine_expiry=medicine_obj.medicine_expiry,
                                                           )
            status = 'success'
        else:
            MedicineStore.objects.filter(query).update(qty=pre_qty)
            MedicineStore.objects.filter(id=obj_id).delete()
            status = 'failed'

        context = {
            'status': status
        }
        return JsonResponse(context)


def transfer_medicine_from_mini(request):
    if request.method == 'POST':
        form = request.POST
        recorde_id = int(form.get('recorde_id'))
        from_store_id = int(form.get('from_store_id'))
        to_store_id = int(form.get('to_store_id'))
        transfer_medicine_qty = int(form.get('transfer_medicine_qty'))
        medicine = MedicineStore.objects.get(id=recorde_id)
        medicine_id = medicine.medicine.id
        medicine_name = medicine.medicine.medicine_name
        existing_qty = medicine.qty
        medicine_manufacturer = medicine.medicine.medicine_manufacturer
        medicine_expiry = medicine.medicine.medicine_expiry

        if existing_qty >= transfer_medicine_qty:
            medicine_qty = existing_qty - transfer_medicine_qty
        else:
            status = 'failed'
            context = {
                'status': status
            }
            return JsonResponse(context)
        query = Q(medicine_id=medicine_id, to_store_id=to_store_id)
        is_medicine = MedicineStore.objects.filter(query)
        if is_medicine:
            pre_qty = is_medicine[0].qty
            total_transfer_qty = pre_qty + transfer_medicine_qty
            obj = MedicineStore.objects.filter(query).update(qty=total_transfer_qty)
        else:
            obj = MedicineStore.objects.create(from_store_id=from_store_id,
                                               to_store_id=to_store_id,
                                               medicine_id=medicine_id,
                                               qty=transfer_medicine_qty,
                                               )
            obj_id = obj.id

        if obj:
            MedicineStore.objects.filter(medicine_id=medicine_id, to_store_id=from_store_id).update(qty=medicine_qty)
            MedicineStoreTransactionHistory.objects.create(from_store_id=from_store_id,
                                                           to_store_id=to_store_id,
                                                           medicine_id=medicine_id,
                                                           medicine_name=medicine_name,
                                                           qty=transfer_medicine_qty,
                                                           medicine_manufacturer=medicine_manufacturer,
                                                           medicine_expiry=medicine_expiry,
                                                           )
            status = 'success'
        else:
            MedicineStore.objects.filter(query).update(qty=pre_qty)
            MedicineStore.objects.filter(id=obj_id).delete()
            status = 'failed'

        context = {
            'status': status
        }
        return JsonResponse(context)


def medicine_stock_history(request):
    transaction = MedicineStoreTransactionHistory.objects.all().order_by('-id')
    if transaction:
        store_name = transaction[0].to_store
    else:
        store_name = ''
    context = {
        'store_name': store_name,
        'transaction': transaction,
    }
    return render(request, 'medicine_stock_history.html', context)


def mini_store(request):
    store = Store.objects.filter(type='MINI').order_by('-id')
    context = {
        'store': store
    }
    return render(request, 'mini_store_detail.html', context)


def view_mini_store_medicine(request, store_id):
    store_medicine = MedicineStore.objects.filter(to_store_id=store_id)
    store_name = Store.objects.filter(id=store_id)
    store_name = store_name[0].user.username
    context = {
        'store_medicine': store_medicine,
        'store_name': store_name
    }
    return render(request, 'mini_store_medicine_detail.html', context)
