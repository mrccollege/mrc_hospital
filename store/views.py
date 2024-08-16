from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from .models import Store, MedicineStore, \
    MedicineStoreTransactionHistory
from medicine.models import Medicine

from account.models import User
from patient.models import Patient

from bill.models import PatientBill, PatientBillDetail


# Create your views here.
def main_store(request):
    store = Store.objects.filter(type='MAIN')
    if store:
        main_store_id = store[0].id
        store_name = store[0].user.username
        medicine = MedicineStore.objects.filter(to_store_id=main_store_id)
    else:
        main_store_id = 0
        medicine = []
        store_name = 'Please create main store.'

    context = {
        'main_store_id': main_store_id,
        'store_name': store_name,
        'medicine': medicine
    }
    return render(request, 'main_store_detail.html', context)


def transfer_main_store_medicine_detail(request, id):
    store_medicine = MedicineStore.objects.get(id=id)
    store_name = store_medicine.to_store.user.username

    mini_store = Store.objects.filter(type='MINI')
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


def transfer_medicine_from_main(request, id):
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
            available_stock = MedicineStore.objects.get(medicine_id=medicine_id, to_store_id=to_store_id)
            medicine_obj = Medicine.objects.get(id=medicine_id)
            MedicineStoreTransactionHistory.objects.create(from_store_id=main_store_id,
                                                           to_store_id=to_store_id,
                                                           medicine_id=medicine_id,
                                                           medicine_name=medicine_name,
                                                           available_qty=available_stock.qty,
                                                           transfer_qty=transfer_medicine_qty,
                                                           medicine_manufacture=medicine_obj.medicine_manufacturer,
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
        medicine_name = medicine.medicine.name
        existing_qty = medicine.qty
        medicine_manufacture = medicine.medicine.manufacture
        medicine_expiry = medicine.expiry
        batch_no = medicine.batch_no
        category = medicine.medicine.category.name
        price = medicine.price

        if existing_qty >= transfer_medicine_qty:
            medicine_qty = existing_qty - transfer_medicine_qty
        else:
            status = 'failed'
            msg = 'Transfer qty is more than Total qty of record.'
            context = {
                'status': status,
                'msg': msg,
            }
            return JsonResponse(context)
        query = Q(medicine_id=medicine_id, to_store_id=to_store_id, batch_no=batch_no)
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
            MedicineStore.objects.filter(medicine_id=medicine_id, to_store_id=from_store_id, batch_no=batch_no).update(
                qty=medicine_qty)
            available_stock = MedicineStore.objects.get(medicine_id=medicine_id, to_store_id=to_store_id)
            MedicineStoreTransactionHistory.objects.create(from_store_id=from_store_id,
                                                           to_store_id=to_store_id,
                                                           medicine_id=medicine_id,
                                                           medicine_name=medicine_name,
                                                           category=category,
                                                           price=price,
                                                           batch_no=batch_no,
                                                           available_qty=available_stock.qty,
                                                           transfer_qty=transfer_medicine_qty,
                                                           medicine_manufacture=medicine_manufacture,
                                                           medicine_expiry=medicine_expiry,
                                                           )
            status = 'success'
            msg = 'Medicine Transfer successfully.'
        else:
            MedicineStore.objects.filter(query).update(qty=pre_qty)
            MedicineStore.objects.filter(id=obj_id).delete()
            status = 'failed'
            msg = 'Medicine Transfer failed'

        context = {
            'status': status,
            'msg': msg,
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


def search_medicine(request):
    user_id = request.session['user_id']
    store = Store.objects.get(user_id=user_id)
    store_id = store.id
    if request.method == 'GET':
        form = request.GET
        search_value = form.get('search_value')
        medicineIds = form.getlist('medicineIds[]')
        medicine = MedicineStore.objects.filter(to_store_id=store_id,
                                                medicine__name__icontains=search_value,
                                                ).exclude(medicine__id__in=medicineIds)
        data_list = []
        for i in medicine:
            data_dict = {}
            data_dict['record_id'] = i.id
            data_dict['medicine_id'] = i.medicine.id
            data_dict['name'] = i.medicine.name.capitalize()
            data_dict['price'] = i.medicine.medicine_price
            data_dict['record_qty'] = i.qty
            data_list.append(data_dict)
        context = {
            'results': data_list,
        }
        return JsonResponse(context)


@login_required(login_url='/account/user_login/')
def create_bill(request):
    user_id = request.session['user_id']
    try:
        store = Store.objects.get(user_id=user_id)
        store_id = store.id
    except:
        pass

    if request.method == 'POST':
        # User.objects.filter(username='rajat').delete()
        form = request.POST
        username = form.get('patient_name')
        mobile = form.get('mobile')
        address = form.get('address')
        email = mobile + '@yopmail.com'
        password = '12345'
        patient_code = datetime.now().strftime("%Y%d%H%M%S")
        obj_id = 0
        status = 'failed'
        msg = 'Patient Registration failed.'

        is_registered = User.objects.filter(mobile=mobile).exists()
        if is_registered:
            context = {
                'status': 'failed',
                'msg': 'this mobile number already exists.',
            }
            return JsonResponse(context)

        user_obj = User.objects.create_user(username=username,
                                            email=email,
                                            password=password,
                                            mobile=mobile,
                                            address=address
                                            )
        if user_obj:
            patient_id = user_obj.id
            obj = Patient.objects.create(user_id=patient_id,
                                         patient_code=patient_code,
                                         )
            if obj:
                obj_id = obj.id

        if obj_id != 0:
            record_id = form.getlist('record_id')
            medicine_id = form.getlist('medicine_id')
            medicine_price = form.getlist('medicine_price')
            record_qty = form.getlist('record_qty')
            sell_qty = form.getlist('sell_qty')
            total_sell_price = form.getlist('total_sell_price')
            invoice_number = datetime.now().strftime("%Y%d%H%M%S")
            obj = PatientBill.objects.create(patient_id=obj_id,
                                             store_id=store_id,
                                             invoice_number=invoice_number,
                                             )
            if obj:
                for i in range(len(medicine_id)):
                    PatientBillDetail.objects.create(patient_bill_id=obj.id,
                                                     medicine_id=medicine_id[i],
                                                     medicine_qty=record_qty[i],
                                                     medicine_sell_qty=sell_qty[i],
                                                     medicine_price=medicine_price[i],
                                                     medicine_sell_price=total_sell_price[i],
                                                     )
                    remaining_qty = int(record_qty[i]) - int(sell_qty[i])
                    obj = MedicineStore.objects.filter(to_store_id=store_id, medicine_id=medicine_id[i]).update(
                        qty=remaining_qty)
                    if obj:
                        medicine = Medicine.objects.get(id=medicine_id)
                        MedicineStoreTransactionHistory.objects.create(from_store_id=store_id,
                                                                       to_store_id=store_id,
                                                                       medicine_id=medicine_id,
                                                                       medicine_name=medicine.medicine_name,
                                                                       available_qty=remaining_qty,
                                                                       sell_qty=sell_qty,
                                                                       medicine_manufacturer=medicine.medicine_manufacturer,
                                                                       medicine_expiry=medicine.medicine_expiry,
                                                                       )

                status = 'success'
                msg = 'Bill Generated Successfully.'

        context = {
            'status': status,
            'msg': msg,
        }
        return JsonResponse(context)
    else:
        return render(request, 'create_bill.html')
