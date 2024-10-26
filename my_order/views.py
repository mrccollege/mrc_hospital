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

from store.models import Store, MedicineStoreTransactionHistory

from my_order.models import MedicineOrderBillHead

from my_order.models import MedicineOrderBillDetail


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
                                                          status=0,
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
    return JsonResponse(context)


@login_required(login_url='/account/user_login/')
def create_bill(request, order_type, id):
    if request.method == 'POST':
        form = request.POST
        print(form, '============form========')
        user_id = request.session['user_id']
        try:
            store = Store.objects.get(user_id=user_id)
            store_id = store.id
        except:
            store_id = 0

        status = 'failed'
        msg = 'Bill Creation failed.'

        invoice_number = datetime.now().strftime("%Y%d%H%M%S")
        medicines = json.loads(request.POST.get('medicines'))
        doctor_id = form.get('doctor_id')
        subtotal = float(form.get('sub_total'))
        sgst = form.get('sgst')
        cgst = form.get('cgst')
        cash = float(form.get('cash'))
        online = float(form.get('online'))
        shipping_packing = int(form.get('shipping_packing'))
        discount = int(form.get('total_discount'))
        total = float(form.get('total'))
        old_credit = float(form.get('old_credit'))
        new_credit = float(form.get('new_credit'))

        # record_id = form.getlist('record_id')
        # medicine_id = form.getlist('medicine_id')
        # record_qty = form.getlist('record_qty')
        # mrp = form.getlist('mrp')
        # discount = form.getlist('discount')
        # sale_rate = form.getlist('sale_rate')
        # hsn = form.getlist('hsn')
        # gst = form.getlist('gst')
        # amount = form.getlist('amount')

        obj = MedicineOrderBillHead.objects.create(doctor_id=doctor_id,
                                                   store_id=store_id,
                                                   invoice_number=invoice_number,
                                                   sgst=sgst,
                                                   cgst=cgst,
                                                   subtotal=subtotal,
                                                   credit=new_credit,
                                                   cash=cash,
                                                   online=online,
                                                   shipping=shipping_packing,
                                                   discount=discount,
                                                   pay_amount=total,
                                                   status=1,
                                                   )
        if obj:
            for medicine_data in medicines:
                medicine_id = medicine_data['medicine_id']
                record_qty = int(medicine_data['record_qty'])
                sell_qty = int(medicine_data['sell_qty'])
                discount = int(medicine_data['discount'])
                mrp = float(medicine_data['mrp'])
                sale_rate = float(medicine_data['sale_rate'])
                amount = float(medicine_data['amount'])

                MedicineOrderBillDetail.objects.create(head_id=obj.id,
                                                       medicine_id=medicine_id,
                                                       record_qty=record_qty,
                                                       sell_qty=sell_qty,
                                                       mrp=mrp,
                                                       discount=discount,
                                                       sale_rate=sale_rate,
                                                       amount=amount,
                                                       )
                if sell_qty < record_qty:
                    remaining_qty = int(record_qty) - int(sell_qty)
                    obj = MedicineStore.objects.filter(to_store_id=store_id, medicine_id=medicine_id).update(
                        qty=remaining_qty)
            MedicineOrderHead.objects.filter(id=id).update(status=1)
            status = 'success'
            msg = 'Bill creation Successfully.'

        context = {
            'status': status,
            'msg': msg,
        }
        return JsonResponse(context)

    else:
        user_id = request.session['user_id']
        try:
            store = Store.objects.get(user_id=user_id)
            store_id = store.id
        except:
            store_id = 0

        user = MedicineOrderHead.objects.get(id=id)
        medicine = MedicineOrderDetail.objects.filter(head_id=id)
        medicine_list = []

        for i in medicine:
            data_dict = {}
            query = Q(to_store_id=store_id, medicine_id=i.medicine.id)
            store_medicine = MedicineStore.objects.filter(query).values('qty', 'price')
            data_dict['medicine_id'] = i.medicine.id
            data_dict['medicine_name'] = i.medicine.name
            data_dict['order_qty'] = i.order_qty

            try:
                data_dict['record_qty'] = store_medicine[0]['qty']
            except:
                data_dict['record_qty'] = 0

            try:
                data_dict['mrp'] = store_medicine[0]['price']
            except:
                data_dict['mrp'] = 0

            medicine_list.append(data_dict)

        context = {
            'id': id,
            'order_type': order_type,
            'store_id': store_id,
            'user': user,
            'medicine': medicine_list,
        }
        if order_type == 1:
            return render(request, 'order_tax_invoice_in_state.html', context)
        elif order_type == 2:
            return render(request, 'order_tax_invoice_other_state.html', context)
        elif order_type == 3:
            return render(request, 'oder_bill_of_supply.html', context)
        else:
            return render(request, 'oder_bill_of_supply.html', context)
