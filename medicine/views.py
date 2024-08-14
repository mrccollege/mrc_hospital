from datetime import datetime

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from .models import Medicine

from store.models import Store, MedicineStore, MedicineStoreTransactionHistory

from common_function.date_formate import convert_date_format


# Create your views here.
def add_new_medicine(request):
    if request.method == 'POST':
        form = request.POST
        store_id = int(form.get('store_id'))
        medicine_name = form.get('medicine_name')
        medicine_price = form.get('medicine_price')
        medicine_qty = form.get('medicine_qty')
        medicine_manufacturer = form.get('medicine_manufacturer')
        medicine_expiry = form.get('medicine_expiry')
        medicine_expiry = convert_date_format(medicine_expiry)
        status = 'failed'
        msg = 'Something went wrong.'
        try:
            store_obj = Store.objects.filter(id=store_id).exists()
            if store_obj:
                medicine_obj = Medicine.objects.create(medicine_name=medicine_name,
                                                       medicine_price=int(medicine_price),
                                                       medicine_manufacturer=medicine_manufacturer,
                                                       medicine_expiry=medicine_expiry,
                                                       )
                if medicine_obj:
                    medicine_id = medicine_obj.id
                    main_store_medicine_obj = MedicineStore.objects.create(from_store_id=store_id,
                                                                           to_store_id=store_id,
                                                                           medicine_id=medicine_id,
                                                                           qty=medicine_qty,
                                                                           )
                    if main_store_medicine_obj:
                        MedicineStoreTransactionHistory.objects.create(from_store_id=store_id,
                                                                       to_store_id=store_id,
                                                                       medicine_id=medicine_id,
                                                                       medicine_name=medicine_name,
                                                                       qty=medicine_qty,
                                                                       medicine_manufacturer=medicine_manufacturer,
                                                                       medicine_expiry=medicine_expiry,
                                                                       )
                        status = 'success'
                        msg = 'Medicine Added Successfully.'
            else:
                status = status
                msg = 'Please Create Main store first.'

        except Exception as e:
            status = status
            msg = str(e)

        context = {
            'status': status,
            'msg': msg,
        }
        return JsonResponse(context)
    else:
        store = Store.objects.all()
        context = {
            'store': store
        }
        return render(request, 'add_medicine.html', context)


def view_main_medicine(request, id):
    medicine_record = MedicineStore.objects.get(id=id)
    context = {
        'medicine': medicine_record
    }
    return render(request, 'update_medicine_record.html', context)


def update_new_medicine(request):
    if request.method == 'POST':
        form = request.POST
        medicine_id = int(form.get('medicine_id'))
        medicine_name = form.get('medicine_name')
        medicine_qty = form.get('medicine_qty')
        add_medicine_qty = form.get('add_medicine_qty')
        minus_medicine_qty = form.get('minus_medicine_qty')
        medicine_manufacturer = form.get('medicine_manufacturer')
        medicine_expiry = form.get('medicine_expiry')
        medicine_expiry = convert_date_format(medicine_expiry)
        status = 'failed'
        msg = 'Medicine not added.'
        try:
            medicine_obj = Medicine.objects.filter(id=medicine_id).update(medicine_name=medicine_name,
                                                                          medicine_manufacturer=medicine_manufacturer,
                                                                          medicine_expiry=medicine_expiry,
                                                                          )
            if medicine_obj:
                store_obj = Store.objects.filter(type='MAIN')
                if store_obj:
                    to_store_id = store_obj[0].id
                    query = Q(medicine_id=medicine_id, to_store_id=to_store_id)
                    obj = MedicineStore.objects.get(query)
                    total_qty = obj.qty
                    if add_medicine_qty:
                        add_medicine_qty = add_medicine_qty
                        total_qty = obj.qty + int(add_medicine_qty)
                    else:
                        add_medicine_qty = 0

                    if minus_medicine_qty:
                        minus_medicine_qty = minus_medicine_qty
                        total_qty = obj.qty - int(minus_medicine_qty)
                    else:
                        minus_medicine_qty = 0
                    main_store_medicine_obj = MedicineStore.objects.filter(query).update(qty=int(total_qty))
                    if main_store_medicine_obj:
                        MedicineStoreTransactionHistory.objects.create(from_store_id=to_store_id,
                                                                       to_store_id=to_store_id,
                                                                       medicine_id=medicine_id,
                                                                       medicine_name=medicine_name,
                                                                       available_qty=total_qty,
                                                                       add_qty=add_medicine_qty,
                                                                       minus_qty=minus_medicine_qty,
                                                                       medicine_manufacturer=medicine_manufacturer,
                                                                       medicine_expiry=medicine_expiry,
                                                                       )
                        status = 'success'
                        msg = 'Medicine Updated Successfully.'

        except Exception as e:
            status = status
            msg = str(e)

        context = {
            'status': status,
            'msg': msg,
        }
        return JsonResponse(context)


def all_medicine(request):
    medicine = Medicine.objects.filter()
    context = {
        'medicine': medicine,
    }
    return render(request, 'all_medicine.html', context)


def medicine_update(request, id):
    if request.method == 'POST':
        form = request.POST
        medicine_name = form.get('medicine_name')
        medicine_price = form.get('medicine_price')
        medicine_manufacturer = form.get('medicine_manufacturer')
        medicine_expiry = form.get('medicine_expiry')
        medicine_expiry = convert_date_format(medicine_expiry)
        msg = 'Medicine Update Failed'
        status = 'Failed'
        try:
            medicine_obj = Medicine.objects.filter(id=id).update(medicine_name=medicine_name,
                                                                 medicine_price=int(medicine_price),
                                                                 medicine_manufacturer=medicine_manufacturer,
                                                                 medicine_expiry=medicine_expiry,
                                                                 )
            if medicine_obj:
                msg = 'Medicine Update Successfully.'
                status = 'success'
        except Exception as e:
            msg = str(e)

        context = {
            'msg': msg,
            'status': status,
        }
        return JsonResponse(context)
    else:
        medicine = Medicine.objects.get(id=id)
        context = {
            'id': id,
            'medicine': medicine
        }
        return render(request, 'update_medicine.html', context)
