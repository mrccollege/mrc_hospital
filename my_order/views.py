import json
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from medicine.models import Medicine

from account.models import User

from store.models import MedicineStore

from my_order.models import MedicineOrderDetail

from doctor.models import Doctor

from my_order.models import MedicineOrderHead

from bill.models import PatientBill, PatientBillDetail
from patient.models import Patient
from store.models import Store, MedicineStoreTransactionHistory


# Create your views here.
def search_medicine(request):
    if request.method == 'GET':
        form = request.GET
        medicineIds = form.getlist('medicineIds[]')
        search_term = form.get('searchTerm', '')
        medicine = Medicine.objects.exclude(id__in=medicineIds)
        medicine = medicine.filter(name__icontains=search_term)
        data_list = []
        for i in medicine:
            medicine = MedicineStore.objects.filter(medicine_id=i.id)
            data_dict = {
                'medicine_id': i.id,
                'name': i.name.capitalize(),
                'category': str(i.category.name),
                'mrp': str(medicine[0].price),
            }
            data_list.append(data_dict)

        context = {
            'results': data_list,
        }

        return JsonResponse(context)


def medicine_order(request):
    if request.method == 'POST':
        form = request.POST
        medicines = json.loads(request.POST.get('medicines'))
        doctor_id = form.get('doctor_id')
        subtotal = form.get('sub_total')
        discount = form.get('total_discount')
        pay_amount = form.get('total')
        try:
            order_head = MedicineOrderHead.objects.create(doctor_id=doctor_id,
                                                          subtotal=subtotal,
                                                          discount=discount,
                                                          pay_amount=pay_amount,
                                                          )

            if order_head:
                for medicine_data in medicines:
                    medicine_id = medicine_data['medicine_id']
                    order_qty = medicine_data['order_qty']
                    mrp = medicine_data['mrp']
                    amount = medicine_data['amount']

                    MedicineOrderDetail.objects.create(head_id=order_head.id,
                                                       medicine_id=medicine_id,
                                                       mrp=mrp,
                                                       order_qty=order_qty,
                                                       amount=amount,
                                                       )

                status = 'success'
                msg = 'order successfully created.'

            else:
                status = 'failed'
                msg = 'order failed.'

        except Exception as e:
            status = 'failed'
            msg = str(e)

        context = {
            'status': status,
            'msg': msg,
        }

        return JsonResponse(context)

    else:
        user_id = request.session.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            doctor = Doctor.objects.get(user_id=user.id)
            doctor_id = doctor.id
            user_id = doctor.user.id
        except:
            doctor = ''
            doctor_id = 0
            user_id = 0

        medicine = Medicine.objects.filter()
        context = {
            'medicine': medicine,
            'user_id': user_id,
            'doctor': doctor,
            'doctor_id': doctor_id,
        }
        return render(request, 'medicine_order.html', context)


def update_medicine_order(request, id):
    if request.method == 'POST':
        form = request.POST
        medicines = json.loads(request.POST.get('medicines'))
        doctor_id = form.get('doctor_id')
        subtotal = form.get('sub_total')
        discount = form.get('total_discount')
        pay_amount = form.get('total')
        try:
            order_head = MedicineOrderHead.objects.filter(id=id, doctor_id=doctor_id).update(subtotal=subtotal,
                                                                                             discount=discount,
                                                                                             pay_amount=pay_amount,
                                                                                             )
            medicine_ids = []
            if order_head:
                for medicine_data in medicines:
                    medicine_id = medicine_data['medicine_id']
                    medicine_ids.append(medicine_id)
                    order_qty = medicine_data['order_qty']
                    mrp = medicine_data['mrp']
                    amount = medicine_data['amount']
                    query = Q(medicine_id=medicine_id, head_id=id)
                    already_obj = MedicineOrderDetail.objects.filter(query)
                    if already_obj:
                        MedicineOrderDetail.objects.filter(query).update(mrp=mrp,
                                                                         order_qty=order_qty,
                                                                         amount=amount,
                                                                         )
                    else:
                        MedicineOrderDetail.objects.create(head_id=id,
                                                           medicine_id=medicine_id,
                                                           mrp=mrp,
                                                           order_qty=order_qty,
                                                           amount=amount,
                                                           )

                    MedicineOrderDetail.objects.filter(head_id=id).exclude(medicine_id__in=medicine_ids).delete()

                status = 'success'
                msg = 'order successfully updated.'

            else:
                status = 'failed'
                msg = 'order failed.'

        except Exception as e:
            status = 'failed'
            msg = str(e)

        context = {
            'status': status,
            'msg': msg,
        }

        return JsonResponse(context)

    else:
        user_id = request.session.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            doctor = Doctor.objects.get(user_id=user.id)
            doctor_id = doctor.id
            user_id = doctor.user.id
        except:
            doctor = ''
            doctor_id = 0
            user_id = 0

        order_head = MedicineOrderHead.objects.get(id=id)
        order_detail = MedicineOrderDetail.objects.filter(head_id=id)
        medicine_ids = MedicineOrderDetail.objects.filter(head_id=id).values_list('medicine__id', flat=True)
        medicine = Medicine.objects.filter().exclude(id__in=medicine_ids)
        context = {
            'id': id,
            'order_head': order_head,
            'order_detail': order_detail,
            'medicine': medicine,
            'user_id': user_id,
            'doctor': doctor,
            'doctor_id': doctor_id,
        }
        return render(request, 'update_medicine_order.html', context)


def my_medicine_ordered_list(request):
    user_id = request.session.get('user_id')
    try:
        user = User.objects.get(id=user_id)
        doctor = Doctor.objects.get(user_id=user.id)
        doctor_id = doctor.id
        user_id = doctor.user.id
    except:
        doctor = ''
        doctor_id = 0
        user_id = 0
    order = MedicineOrderHead.objects.filter(doctor_id=doctor_id)
    context = {
        'order': order,
    }
    return render(request, 'my_odered_list.html', context)


def delete_medicine_order(request, id):
    user_id = request.session.get('user_id')
    try:
        user = User.objects.get(id=user_id)
        doctor = Doctor.objects.get(user_id=user.id)
        doctor_id = doctor.id
    except:
        doctor_id = 0

    if doctor_id != 0:
        MedicineOrderHead.objects.filter(id=id).delete()
        MedicineOrderDetail.objects.filter(head_id=id).delete()

        status = 'success'
        msg = 'data deleted'
    else:
        status = 'failed'
        msg = 'data not deleted'

    context = {
        'status': status,
        'msg': msg,
    }
    print(context, '==========context')
    return JsonResponse(context)


@login_required(login_url='/account/user_login/')
def create_bill(request, order_type, id):
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
        user = MedicineOrderHead.objects.get(id=id)
        medicine = MedicineOrderDetail.objects.filter(head_id=id)

        context = {
            'user': user,
            'medicine': medicine,
        }

        if order_type == 1:
            return render(request, 'order_tax_invoice_in_state.html', context)
        elif order_type == 2:
            return render(request, 'order_tax_invoice_other_state.html', context)
        elif order_type == 3:
            return render(request, 'oder_bill_of_supply.html', context)
        else:
            return render(request, 'oder_bill_of_supply.html', context)
