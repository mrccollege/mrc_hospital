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

from bill.models import SGST, CGST


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
        transfer_medicine_qty = int(form.get('transfer_medicine_qty'))
        medicine = MedicineStore.objects.get(id=id)
        main_store_id = medicine.to_store.id

        medicine_name = medicine.medicine.name
        existing_qty = medicine.qty

        category = medicine.medicine.category.name
        price = medicine.price
        batch_no = medicine.batch_no

        medicine_manufacture = medicine.medicine.manufacture
        medicine_expiry = medicine.expiry

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
                                               price=price,
                                               batch_no=batch_no,
                                               expiry=medicine_expiry
                                               )
            obj_id = obj.id

        if obj:
            MedicineStore.objects.filter(medicine_id=medicine_id, to_store_id=main_store_id).update(qty=medicine_qty)
            available_stock = MedicineStore.objects.get(medicine_id=medicine_id, to_store_id=to_store_id)
            MedicineStoreTransactionHistory.objects.create(from_store_id=main_store_id,
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
                                               price=price,
                                               batch_no=batch_no,
                                               expiry=medicine_expiry
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
    if request.method == 'GET':
        form = request.GET
        search_value = form.get('search_value', '').strip()
        medicineIds = form.getlist('medicineIds[]')

        try:
            user_id = request.session['user_id']
            store = Store.objects.get(user_id=user_id)
            store_id = store.id
        except:
            pass

        query = Q(to_store_id=store_id) & ~Q(medicine__id__in=medicineIds)
        if search_value:
            search_terms = search_value.split()
            for term in search_terms:
                query &= Q(medicine__name__icontains=term)

        medicines = MedicineStore.objects.filter(query).values('id', 'medicine__id', 'medicine__name', 'price', 'qty')
        data_list = [
            {
                'record_id': i['id'],
                'medicine_id': i['medicine__id'],
                'name': i['medicine__name'].capitalize(),
                'price': i['price'],
                'record_qty': i['qty'],
            }
            for i in medicines
        ]
        context = {'results': data_list}
        return JsonResponse(context)


@login_required(login_url='/account/user_login/')
def create_bill(request):
    if request.method == 'POST':
        # User.objects.filter(username='rajat').delete()
        form = request.POST
        user_id = request.session['user_id']
        try:
            store = Store.objects.get(user_id=user_id)
            store_id = store.id
        except:
            store_id = 0
        username = form.get('patient_name')
        mobile = form.get('mobile')
        address = form.get('address')
        email = mobile + '@yopmail.com'
        password = '12345'
        patient_code = datetime.now().strftime("%Y%d%H%M%S")
        obj_id = 0
        status = 'failed'
        msg = 'Patient Registration failed.'

        is_registered = User.objects.filter(mobile=mobile)
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
                                            address=address, )
        if user_obj:
            patient_id = user_obj.id
            obj = Patient.objects.create(user_id=patient_id,
                                         patient_code=patient_code, )
            if obj:
                obj_id = obj.id

        if obj_id != 0:
            invoice_number = datetime.now().strftime("%Y%d%H%M%S")
            sgst = form.get('sgst')
            cgst = form.get('cgst')
            credit = form.get('credit')
            cash = form.get('cash')
            online = form.get('online')
            shipping_packing = form.get('shipping_packing')
            discount = form.get('discount')
            total = form.get('total')

            obj = PatientBill.objects.create(patient_id=obj_id,
                                             store_id=store_id,
                                             invoice_number=invoice_number,
                                             sgst=sgst,
                                             cgst=cgst,
                                             credit=credit,
                                             cash=cash,
                                             online=online,
                                             shipping_packing=shipping_packing,
                                             discount=discount,
                                             total=total, )
            if obj:
                record_id = form.getlist('record_id')
                medicine_id = form.getlist('medicine_id')
                record_qty = form.getlist('record_qty')
                sell_qty = form.getlist('sell_qty')
                mrp = form.getlist('mrp')
                discount = form.getlist('discount')
                sale_rate = form.getlist('sale_rate')
                hsn = form.getlist('hsn')
                gst = form.getlist('gst')
                amount = form.getlist('amount')

                for i in range(len(medicine_id)):
                    PatientBillDetail.objects.create(patient_bill_id=obj.id,
                                                     medicine_id=medicine_id[i],
                                                     record_qty=record_qty[i],
                                                     sell_qty=sell_qty[i],
                                                     mrp=mrp[i],
                                                     discount=discount[i],
                                                     sale_rate=sale_rate[i],
                                                     hsn=hsn[i],
                                                     gst=gst[i],
                                                     amount=amount[i],
                                                     )
                    remaining_qty = int(record_qty[i]) - int(sell_qty[i])
                    obj = MedicineStore.objects.filter(to_store_id=store_id, medicine_id=medicine_id[i]).update(
                        qty=remaining_qty)
                    if obj:
                        medicine = MedicineStore.objects.get(id=record_id)
                        MedicineStoreTransactionHistory.objects.create(from_store_id=store_id,
                                                                       to_store_id=store_id,
                                                                       medicine_id=medicine_id,
                                                                       medicine_name=medicine.medicine.name,
                                                                       category=medicine.category,
                                                                       price=medicine.price,
                                                                       batch_no=medicine.batch_no,
                                                                       available_qty=remaining_qty,
                                                                       sell_qty=sell_qty[i],
                                                                       medicine_manufacture=medicine.manufacture,
                                                                       medicine_expiry=medicine.expiry,
                                                                       )

                status = 'success'
                msg = 'Bill Generated Successfully.'

        context = {
            'status': status,
            'msg': msg,
        }
        return JsonResponse(context)
    else:
        sgst = SGST.objects.all()
        cgst = CGST.objects.all()

        context = {
            'sgst': sgst,
            'cgst': cgst,
        }
        # return render(request, 'tax_invoice_in_state.html', context)
        # return render(request, 'tax_invoice_other_state.html', context)
        return render(request, 'bill_of_supply.html', context)
