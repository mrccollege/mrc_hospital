import json
from datetime import datetime
from django.db.models import Case, When
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from medicine.models import Medicine
from django.db.models import Max
from account.models import User

from store.models import MedicineStore

from my_order.models import MedicineOrderDetail

from doctor.models import Doctor

from my_order.models import MedicineOrderHead

from store.models import Store, MedicineStoreTransactionHistory

from my_order.models import MedicineOrderBillHead, MedicineOrderBillDetail, MedicineUnregisteredOrderBillHead, \
    MedicineUnregisteredOrderBillDetail

from my_order.models import EstimateMedicineOrderBillHead, EstimateMedicineOrderBillDetail
from django.db.models import Sum, F, FloatField, ExpressionWrapper
from order_payment_detail.models import PaymentDetail
from django.db.models.functions import Coalesce
from decimal import Decimal
from my_order.models import InvoiceTracker, NormalInvoiceTracker, EstimateInvoiceTracker
from django.db.models import DecimalField

from my_order.models import DirectEstimateHead, DirectEstimateDetail


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


def generate_invoice_number():
    obj, _ = InvoiceTracker.objects.get_or_create(year=datetime.now().year)
    invoice_number = obj.get_next_invoice_number()
    return invoice_number


def medicine_order(request):
    if request.method == 'POST':
        form = request.POST
        medicines = json.loads(request.POST.get('medicines'))
        doctor_id = form.get('doctor_id')
        subtotal = form.get('sub_total')
        discount = form.get('total_discount')
        pay_amount = form.get('total')
        invoice_number = 'Mrc'
        try:
            order_head = MedicineOrderHead.objects.create(invoice_number=invoice_number,
                                                          doctor_id=doctor_id,
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

        medicine = Medicine.objects.filter(recom_to_doctor=True)
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
    except:
        doctor_id = 0

    order = MedicineOrderHead.objects.filter(doctor_id=doctor_id).order_by('-id')
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


def normal_generate_invoice_number():
    obj, _ = NormalInvoiceTracker.objects.get_or_create(year=datetime.now().year)
    invoice_number = obj.get_next_invoice_number()
    return invoice_number


@login_required(login_url='/account/user_login/')
def direct_estimate_bill(request, order_type, id):
    if request.method == 'POST':
        form = request.POST
        user_id = request.session['user_id']
        try:
            store = Store.objects.get(user_id=user_id)
            store_id = store.id
        except:
            store_id = 0

        status = 'failed'
        msg = 'Bill Creation failed.'

        medicines = json.loads(request.POST.get('medicines'))
        invoice_number = normal_generate_invoice_number()
        doctor_id = form.get('doctor_id')

        subtotal = float(form.get('sub_total'))
        discount = int(form.get('total_discount'))
        shipping_packing = float(form.get('shipping_packing'))

        discount_amount = subtotal * discount / 100
        after_dis_amount = subtotal - discount_amount + shipping_packing

        cash = float(form.get('cash'))
        online = float(form.get('online'))

        sgst = form.get('sgst')
        cgst = form.get('cgst')

        obj = DirectEstimateHead.objects.create(order_id_id=id,
                                                invoice_number=invoice_number,
                                                doctor_id=doctor_id,
                                                store_id=store_id,
                                                sgst=sgst,
                                                cgst=cgst,
                                                subtotal=subtotal,
                                                discount_amount=discount_amount,
                                                cash=cash,
                                                online=online,
                                                shipping=shipping_packing,
                                                discount=discount,
                                                pay_amount=after_dis_amount,
                                                current=after_dis_amount,
                                                status=1,
                                                order_type=order_type,
                                                )
        if obj:
            head_id = obj.id
            for medicine_data in medicines:
                medicine_id = medicine_data['medicine_id']
                record_qty = int(medicine_data['record_qty'])
                sell_qty = int(medicine_data['sell_qty'])
                order_qty = int(medicine_data['order_qty'])
                discount = int(medicine_data['discount'])
                mrp = float(medicine_data['mrp'])
                sale_rate = float(medicine_data['sale_rate'])
                try:
                    hsn = medicine_data['hsn']
                except:
                    hsn = ''

                try:
                    gst = int(medicine_data['gst'])
                except:
                    gst = 0

                try:
                    taxable_amount = float(medicine_data['taxable_amount'])
                except:
                    taxable_amount = 0

                try:
                    tax = float(medicine_data['tax'])
                except:
                    tax = 0

                amount = float(medicine_data['amount'])

                obj = DirectEstimateDetail.objects.create(head_id=head_id,
                                                          medicine_id=medicine_id,
                                                          record_qty=record_qty,
                                                          sell_qty=sell_qty,
                                                          order_qty=order_qty,
                                                          mrp=mrp,
                                                          discount=discount,
                                                          sale_rate=sale_rate,
                                                          hsn=hsn,
                                                          gst=gst,
                                                          taxable_amount=taxable_amount,
                                                          tax=tax,
                                                          amount=amount,
                                                          )

                if obj:
                    if sell_qty <= record_qty:
                        remaining_qty = int(record_qty) - int(sell_qty)
                        MedicineStore.objects.filter(to_store_id=store_id, medicine_id=medicine_id).update(
                            qty=remaining_qty)
                        DirectEstimateDetail.objects.filter(id=obj.id).update(record_qty=remaining_qty)
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

        cash_online_amount = DirectEstimateHead.objects.filter(doctor_id=user.doctor.id).aggregate(
            total=Sum(
                Coalesce(F('cash'), 0) +
                Coalesce(F('online'), 0) +
                Coalesce(F('extra_cash_amount'), 0) +
                Coalesce(F('extra_online_amount'), 0),
                output_field=DecimalField()
            )
        )['total'] or 0

        total_pay_amount = DirectEstimateHead.objects.filter(doctor_id=user.doctor.id).aggregate(
            total=Sum('pay_amount')
        )['total'] or 0

        old_credit_sum = total_pay_amount - cash_online_amount

        medicine = MedicineOrderDetail.objects.filter(head_id=id)
        medicine_list = []

        for i in medicine:
            data_dict = {}
            query = Q(to_store_id=store_id, medicine_id=i.medicine.id)
            store_medicine = MedicineStore.objects.filter(query).values('qty', 'price', 'expiry')
            data_dict['medicine_id'] = i.medicine.id
            data_dict['medicine_name'] = i.medicine.name
            data_dict['order_qty'] = i.order_qty
            data_dict['hsn'] = i.medicine.hsn
            data_dict['gst'] = i.medicine.gst
            data_dict['gst'] = i.medicine.gst
            try:
                data_dict['expiry'] = store_medicine[0]['expiry']
            except:
                data_dict['expiry'] = ''
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
            'invoice_number': user.invoice_number,
            'medicine': medicine_list,
            'old_credit_sum': old_credit_sum,
        }
        return render(request, 'normal_bill/direct_estimate.html', context)


@login_required(login_url='/account/user_login/')
def create_bill(request, order_type, id):
    if request.method == 'POST':
        form = request.POST
        user_id = request.session['user_id']
        try:
            store = Store.objects.get(user_id=user_id)
            store_id = store.id
        except:
            store_id = 0

        status = 'failed'
        msg = 'Bill Creation failed.'

        medicines = json.loads(request.POST.get('medicines'))
        invoice_number = normal_generate_invoice_number()
        doctor_id = form.get('doctor_id')

        subtotal = float(form.get('sub_total'))
        discount = int(form.get('total_discount'))
        shipping_packing = float(form.get('shipping_packing'))

        discount_amount = subtotal * discount / 100
        after_dis_amount = subtotal - discount_amount + shipping_packing

        cash = float(form.get('cash'))
        online = float(form.get('online'))

        sgst = form.get('sgst')
        cgst = form.get('cgst')

        obj = MedicineOrderBillHead.objects.create(order_id_id=id,
                                                   invoice_number=invoice_number,
                                                   doctor_id=doctor_id,
                                                   store_id=store_id,
                                                   sgst=sgst,
                                                   cgst=cgst,
                                                   subtotal=subtotal,
                                                   discount_amount=discount_amount,
                                                   cash=cash,
                                                   online=online,
                                                   shipping=shipping_packing,
                                                   discount=discount,
                                                   pay_amount=after_dis_amount,
                                                   current=after_dis_amount,
                                                   status=1,
                                                   order_type=order_type,
                                                   )
        if obj:
            head_id = obj.id
            for medicine_data in medicines:
                medicine_id = medicine_data['medicine_id']
                record_qty = int(medicine_data['record_qty'])
                sell_qty = int(medicine_data['sell_qty'])
                order_qty = int(medicine_data['order_qty'])
                discount = int(medicine_data['discount'])
                mrp = float(medicine_data['mrp'])
                sale_rate = float(medicine_data['sale_rate'])
                try:
                    hsn = medicine_data['hsn']
                except:
                    hsn = ''

                try:
                    gst = int(medicine_data['gst'])
                except:
                    gst = 0

                try:
                    taxable_amount = float(medicine_data['taxable_amount'])
                except:
                    taxable_amount = 0

                try:
                    tax = float(medicine_data['tax'])
                except:
                    tax = 0

                amount = float(medicine_data['amount'])

                obj = MedicineOrderBillDetail.objects.create(head_id=head_id,
                                                             medicine_id=medicine_id,
                                                             record_qty=record_qty,
                                                             sell_qty=sell_qty,
                                                             order_qty=order_qty,
                                                             mrp=mrp,
                                                             discount=discount,
                                                             sale_rate=sale_rate,
                                                             hsn=hsn,
                                                             gst=gst,
                                                             taxable_amount=taxable_amount,
                                                             tax=tax,
                                                             amount=amount,
                                                             )

                if obj:
                    if sell_qty <= record_qty:
                        remaining_qty = int(record_qty) - int(sell_qty)
                        MedicineStore.objects.filter(to_store_id=store_id, medicine_id=medicine_id).update(
                            qty=remaining_qty)
                        MedicineOrderBillDetail.objects.filter(id=obj.id).update(record_qty=remaining_qty)
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

        cash_online_amount = MedicineOrderBillHead.objects.filter(doctor_id=user.doctor.id).aggregate(
            total=Sum(
                Coalesce(F('cash'), 0) +
                Coalesce(F('online'), 0) +
                Coalesce(F('extra_cash_amount'), 0) +
                Coalesce(F('extra_online_amount'), 0),
                output_field=DecimalField()
            )
        )['total'] or 0

        total_pay_amount = MedicineOrderBillHead.objects.filter(doctor_id=user.doctor.id).aggregate(
            total=Sum('pay_amount')
        )['total'] or 0

        old_credit_sum = total_pay_amount - cash_online_amount

        medicine = MedicineOrderDetail.objects.filter(head_id=id)
        medicine_list = []

        for i in medicine:
            data_dict = {}
            query = Q(to_store_id=store_id, medicine_id=i.medicine.id)
            store_medicine = MedicineStore.objects.filter(query).values('qty', 'price', 'expiry')
            data_dict['medicine_id'] = i.medicine.id
            data_dict['medicine_name'] = i.medicine.name
            data_dict['order_qty'] = i.order_qty
            data_dict['hsn'] = i.medicine.hsn
            data_dict['gst'] = i.medicine.gst
            data_dict['gst'] = i.medicine.gst
            try:
                data_dict['expiry'] = store_medicine[0]['expiry']
            except:
                data_dict['expiry'] = ''
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
            'invoice_number': user.invoice_number,
            'medicine': medicine_list,
            'old_credit_sum': old_credit_sum,
        }
        if order_type == 1:
            return render(request, 'normal_bill/order_tax_invoice_in_state.html', context)
        elif order_type == 2:
            return render(request, 'normal_bill/order_tax_invoice_other_state.html', context)
        elif order_type == 3:
            return render(request, 'normal_bill/oder_bill_of_supply.html', context)
        else:
            return render(request, 'normal_bill/oder_bill_of_supply.html', context)


@login_required(login_url='/account/user_login/')
def unregistered_create_bill(request, order_type, id):
    if request.method == 'POST':
        form = request.POST
        user_id = request.session['user_id']
        try:
            store = Store.objects.get(user_id=user_id)
            store_id = store.id
        except:
            store_id = 0

        status = 'failed'
        msg = 'Bill Creation failed.'

        medicines = json.loads(request.POST.get('medicines'))
        invoice_number = generate_invoice_number()
        doctor_id = form.get('doctor_id')

        subtotal = float(form.get('sub_total'))
        discount = int(form.get('total_discount'))
        shipping_packing = float(form.get('shipping_packing'))

        discount_amount = subtotal * discount / 100
        after_dis_amount = subtotal - discount_amount + shipping_packing

        cash = float(form.get('cash'))
        online = float(form.get('online'))

        sgst = form.get('sgst')
        cgst = form.get('cgst')
        state_code = form.get('state_code')
        is_already = MedicineUnregisteredOrderBillHead.objects.filter(head_id=id)
        if is_already:
            head_id = is_already[0].id
            MedicineUnregisteredOrderBillDetail.objects.filter(head_id=head_id).delete()
            MedicineUnregisteredOrderBillHead.objects.filter(head_id=id).delete()
            MedicineOrderBillHead.objects.filter(id=id).update(final_bill_status=0)

        obj_order_id = MedicineOrderBillHead.objects.get(id=id)
        order_id = obj_order_id.order_id_id
        obj = MedicineUnregisteredOrderBillHead.objects.create(head_id=id,
                                                               order_id_id=order_id,
                                                               invoice_number=invoice_number,
                                                               doctor_id=doctor_id,
                                                               store_id=store_id,
                                                               sgst=sgst,
                                                               cgst=cgst,
                                                               subtotal=subtotal,
                                                               discount_amount=discount_amount,
                                                               cash=cash,
                                                               online=online,
                                                               shipping=shipping_packing,
                                                               discount=discount,
                                                               pay_amount=after_dis_amount,
                                                               current=after_dis_amount,
                                                               status=1,
                                                               order_type=order_type,
                                                               state_code=state_code,
                                                               )
        if obj:
            head_id = obj.id
            for medicine_data in medicines:
                medicine_id = medicine_data['medicine_id']
                record_qty = int(medicine_data['record_qty'])
                sell_qty = int(medicine_data['sell_qty'])
                discount = int(medicine_data['discount'])
                mrp = float(medicine_data['mrp'])
                sale_rate = float(medicine_data['sale_rate'])
                try:
                    hsn = medicine_data['hsn']
                except:
                    hsn = ''

                try:
                    gst = int(medicine_data['gst'])
                except:
                    gst = 0

                try:
                    taxable_amount = float(medicine_data['taxable_amount'])
                except:
                    taxable_amount = 0

                try:
                    tax = float(medicine_data['tax'])
                except:
                    tax = 0

                amount = float(medicine_data['amount'])

                obj = MedicineUnregisteredOrderBillDetail.objects.create(head_id=head_id,
                                                                         medicine_id=medicine_id,
                                                                         record_qty=record_qty,
                                                                         sell_qty=sell_qty,
                                                                         mrp=mrp,
                                                                         discount=discount,
                                                                         sale_rate=sale_rate,
                                                                         hsn=hsn,
                                                                         gst=gst,
                                                                         taxable_amount=taxable_amount,
                                                                         tax=tax,
                                                                         amount=amount,
                                                                         )
                MedicineOrderBillHead.objects.filter(id=id).update(final_bill_status=1)
                if obj:
                    status = 'success'
                    msg = 'Bill creation Successfully.'

        context = {
            'status': status,
            'msg': msg,
        }
        return JsonResponse(context)


@login_required(login_url='/account/user_login/')
def update_medicine_order_bill(request, order_type, id):
    if request.method == 'POST':
        form = request.POST
        user_id = request.session['user_id']
        try:
            store = Store.objects.get(user_id=user_id)
            store_id = store.id
        except:
            store_id = 0

        status = 'failed'
        msg = 'Bill Creation failed.'
        medicines = json.loads(request.POST.get('medicines'))

        subtotal = float(form.get('sub_total'))
        discount1 = int(form.get('total_discount'))
        shipping_packing = float(form.get('shipping_packing'))

        discount_amount = subtotal * discount1 / 100
        after_dis_amount = subtotal - discount_amount + shipping_packing

        cash = float(form.get('cash'))
        online = float(form.get('online'))

        sgst = form.get('sgst')
        cgst = form.get('cgst')
        state_code = form.get('state_code')

        head_id = id

        medicine_ids = []
        for medicine_data in medicines:
            medicine_id = medicine_data['medicine_id']
            medicine_ids.append(medicine_id)
            record_qty = int(medicine_data['record_qty'])
            sell_qty = int(medicine_data['sell_qty'])
            order_qty = int(medicine_data['order_qty'])
            discount = int(medicine_data['discount'])
            mrp = float(medicine_data['mrp'])
            sale_rate = float(medicine_data['sale_rate'])
            try:
                hsn = medicine_data['hsn']
            except:
                hsn = 0

            try:
                gst = int(medicine_data['gst'])
            except:
                gst = 0

            try:
                taxable_amount = float(medicine_data['taxable_amount'])
            except:
                taxable_amount = 0

            try:
                tax = float(medicine_data['tax'])
            except:
                tax = 0
            amount = float(medicine_data['amount'])

            query = Q(head_id=head_id, medicine_id=medicine_id)
            already_obj = MedicineOrderBillDetail.objects.filter(query)

            if already_obj:
                pre_sell_qty = already_obj[0].sell_qty
                update_record_qty = int(record_qty + pre_sell_qty)
                MedicineStore.objects.filter(to_store_id=store_id, medicine_id=medicine_id).update(
                    qty=update_record_qty)
                store_record = MedicineStore.objects.filter(to_store_id=store_id, medicine_id=medicine_id)
                if store_record[0].qty >= sell_qty:
                    record_qty = int(store_record[0].qty) - sell_qty
                    MedicineOrderBillDetail.objects.filter(query).update(record_qty=record_qty,
                                                                         sell_qty=sell_qty,
                                                                         order_qty=order_qty,
                                                                         mrp=mrp,
                                                                         discount=discount,
                                                                         sale_rate=sale_rate,
                                                                         hsn=hsn,
                                                                         gst=gst,
                                                                         taxable_amount=taxable_amount,
                                                                         tax=tax,
                                                                         amount=amount,
                                                                         )

                    MedicineStore.objects.filter(to_store_id=store_id, medicine_id=medicine_id).update(
                        qty=record_qty)
            else:
                store_record = MedicineStore.objects.filter(to_store_id=store_id, medicine_id=medicine_id)
                if store_record[0].qty >= sell_qty:
                    record_qty = int(store_record[0].qty) - sell_qty
                    MedicineOrderBillDetail.objects.create(head_id=head_id,
                                                           medicine_id=medicine_id,
                                                           record_qty=record_qty,
                                                           sell_qty=sell_qty,
                                                           order_qty=order_qty,
                                                           mrp=mrp,
                                                           discount=discount,
                                                           sale_rate=sale_rate,
                                                           hsn=hsn,
                                                           gst=gst,
                                                           taxable_amount=taxable_amount,
                                                           tax=tax,
                                                           amount=amount,
                                                           )
                    MedicineStore.objects.filter(to_store_id=store_id, medicine_id=medicine_id).update(qty=record_qty)

        obj = MedicineOrderBillHead.objects.filter(id=id).update(store_id=store_id,
                                                                 sgst=sgst,
                                                                 cgst=cgst,
                                                                 subtotal=subtotal,
                                                                 cash=cash,
                                                                 online=online,
                                                                 shipping=shipping_packing,
                                                                 discount=discount1,
                                                                 discount_amount=discount_amount,
                                                                 pay_amount=after_dis_amount,
                                                                 current=after_dis_amount,
                                                                 state_code=state_code,
                                                                 )
        if obj:
            MedicineOrderHead.objects.filter(id=id).update(status=1)
            MedicineOrderBillDetail.objects.filter(head_id=id).exclude(medicine_id__in=medicine_ids).delete()
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

        user = MedicineOrderBillHead.objects.get(id=id)
        is_last = user.id == MedicineOrderBillHead.objects.filter(doctor_id=user.doctor.id).aggregate(Max('id'))[
            'id__max']
        is_estimated = EstimateMedicineOrderBillHead.objects.filter(order_id_id=user.order_id).exists()
        if is_last and is_estimated == False:
            is_last = True
        else:
            is_last = False
        cash_online_amount = MedicineOrderBillHead.objects.filter(doctor_id=user.doctor.id).exclude(id=id).aggregate(
            total=Sum(
                Coalesce(F('cash'), 0) +
                Coalesce(F('online'), 0) +
                Coalesce(F('extra_cash_amount'), 0) +
                Coalesce(F('extra_online_amount'), 0),
                output_field=DecimalField()
            )
        )['total'] or 0

        total_pay_amount = MedicineOrderBillHead.objects.filter(doctor_id=user.doctor.id).exclude(id=id).aggregate(
            total=Sum('pay_amount')
        )['total'] or 0

        old_credit_sum = total_pay_amount - cash_online_amount

        medicine = MedicineOrderBillDetail.objects.filter(head_id=id)
        medicine_list = []

        for i in medicine:
            data_dict = {}
            query = Q(to_store_id=store_id, medicine_id=i.medicine.id)
            store_medicine = MedicineStore.objects.filter(query).values('qty', 'price', 'expiry')
            data_dict['medicine_id'] = i.medicine.id
            data_dict['medicine_name'] = i.medicine.name
            data_dict['record_qty'] = i.record_qty
            data_dict['sell_qty'] = i.sell_qty
            data_dict['order_qty'] = i.order_qty
            data_dict['discount'] = i.discount
            data_dict['hsn'] = i.hsn
            data_dict['gst'] = i.gst
            data_dict['taxable_amount'] = i.taxable_amount
            data_dict['tax'] = i.tax
            data_dict['expiry'] = store_medicine[0]['expiry']

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
            'old_credit_sum': old_credit_sum,
            'is_last': is_last,
        }

        if order_type == 1:
            return render(request, 'normal_bill/update_medicine_order_bill_instate.html', context)
        elif order_type == 2:
            return render(request, 'normal_bill/update_medicine_order_bill_other_state.html', context)
        elif order_type == 3:
            return render(request, 'normal_bill/update_order_bill_of_supply.html', context)
        else:
            return (render(request, 'normal_bill/update_order_bill_of_supply.html', context)

                    @ login_required(login_url='/account/user_login/'))


def update_estimate_detail(request, order_type, id):
    if request.method == 'POST':
        form = request.POST
        user_id = request.session['user_id']
        try:
            store = Store.objects.get(user_id=user_id)
            store_id = store.id
        except:
            store_id = 0

        status = 'failed'
        msg = 'Bill Creation failed.'
        medicines = json.loads(request.POST.get('medicines'))

        subtotal = float(form.get('sub_total'))
        discount1 = int(form.get('total_discount'))
        shipping_packing = float(form.get('shipping_packing'))

        discount_amount = subtotal * discount1 / 100
        after_dis_amount = subtotal - discount_amount + shipping_packing

        cash = float(form.get('cash'))
        online = float(form.get('online'))

        sgst = form.get('sgst')
        cgst = form.get('cgst')
        state_code = form.get('state_code')

        head_id = id

        medicine_ids = []
        for medicine_data in medicines:
            medicine_id = medicine_data['medicine_id']
            medicine_ids.append(medicine_id)
            record_qty = int(medicine_data['record_qty'])
            sell_qty = int(medicine_data['sell_qty'])
            order_qty = int(medicine_data['order_qty'])
            discount = int(medicine_data['discount'])
            mrp = float(medicine_data['mrp'])
            sale_rate = float(medicine_data['sale_rate'])
            try:
                hsn = medicine_data['hsn']
            except:
                hsn = 0

            try:
                gst = int(medicine_data['gst'])
            except:
                gst = 0

            try:
                taxable_amount = float(medicine_data['taxable_amount'])
            except:
                taxable_amount = 0

            try:
                tax = float(medicine_data['tax'])
            except:
                tax = 0
            amount = float(medicine_data['amount'])

            query = Q(head_id=head_id, medicine_id=medicine_id)
            already_obj = DirectEstimateDetail.objects.filter(query)

            if already_obj:
                pre_sell_qty = already_obj[0].sell_qty
                update_record_qty = int(record_qty + pre_sell_qty)
                MedicineStore.objects.filter(to_store_id=store_id, medicine_id=medicine_id).update(
                    qty=update_record_qty)
                store_record = MedicineStore.objects.filter(to_store_id=store_id, medicine_id=medicine_id)
                if store_record[0].qty >= sell_qty:
                    record_qty = int(store_record[0].qty) - sell_qty
                    DirectEstimateDetail.objects.filter(query).update(record_qty=record_qty,
                                                                      sell_qty=sell_qty,
                                                                      order_qty=order_qty,
                                                                      mrp=mrp,
                                                                      discount=discount,
                                                                      sale_rate=sale_rate,
                                                                      hsn=hsn,
                                                                      gst=gst,
                                                                      taxable_amount=taxable_amount,
                                                                      tax=tax,
                                                                      amount=amount,
                                                                      )

                    MedicineStore.objects.filter(to_store_id=store_id, medicine_id=medicine_id).update(
                        qty=record_qty)
            else:
                store_record = MedicineStore.objects.filter(to_store_id=store_id, medicine_id=medicine_id)
                if store_record[0].qty >= sell_qty:
                    record_qty = int(store_record[0].qty) - sell_qty
                    DirectEstimateDetail.objects.create(head_id=head_id,
                                                        medicine_id=medicine_id,
                                                        record_qty=record_qty,
                                                        sell_qty=sell_qty,
                                                        order_qty=order_qty,
                                                        mrp=mrp,
                                                        discount=discount,
                                                        sale_rate=sale_rate,
                                                        hsn=hsn,
                                                        gst=gst,
                                                        taxable_amount=taxable_amount,
                                                        tax=tax,
                                                        amount=amount,
                                                        )
                    MedicineStore.objects.filter(to_store_id=store_id, medicine_id=medicine_id).update(qty=record_qty)

        obj = DirectEstimateHead.objects.filter(id=id).update(store_id=store_id,
                                                              sgst=sgst,
                                                              cgst=cgst,
                                                              subtotal=subtotal,
                                                              cash=cash,
                                                              online=online,
                                                              shipping=shipping_packing,
                                                              discount=discount1,
                                                              discount_amount=discount_amount,
                                                              pay_amount=after_dis_amount,
                                                              current=after_dis_amount,
                                                              state_code=state_code,
                                                              )
        if obj:
            MedicineOrderHead.objects.filter(id=id).update(status=1)
            DirectEstimateDetail.objects.filter(head_id=id).exclude(medicine_id__in=medicine_ids).delete()
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

        user = DirectEstimateHead.objects.get(id=id)
        is_last = user.id == DirectEstimateHead.objects.filter(doctor_id=user.doctor.id).aggregate(Max('id'))[
            'id__max']
        is_estimated = EstimateMedicineOrderBillHead.objects.filter(order_id_id=user.order_id).exists()
        if is_last and is_estimated == False:
            is_last = True
        else:
            is_last = False
        cash_online_amount = DirectEstimateHead.objects.filter(doctor_id=user.doctor.id).exclude(id=id).aggregate(
            total=Sum(
                Coalesce(F('cash'), 0) +
                Coalesce(F('online'), 0) +
                Coalesce(F('extra_cash_amount'), 0) +
                Coalesce(F('extra_online_amount'), 0),
                output_field=DecimalField()
            )
        )['total'] or 0

        total_pay_amount = DirectEstimateHead.objects.filter(doctor_id=user.doctor.id).exclude(id=id).aggregate(
            total=Sum('pay_amount')
        )['total'] or 0

        old_credit_sum = total_pay_amount - cash_online_amount

        medicine = DirectEstimateDetail.objects.filter(head_id=id)
        medicine_list = []

        for i in medicine:
            data_dict = {}
            query = Q(to_store_id=store_id, medicine_id=i.medicine.id)
            store_medicine = MedicineStore.objects.filter(query).values('qty', 'price', 'expiry')
            data_dict['medicine_id'] = i.medicine.id
            data_dict['medicine_name'] = i.medicine.name
            data_dict['record_qty'] = i.record_qty
            data_dict['sell_qty'] = i.sell_qty
            data_dict['order_qty'] = i.order_qty
            data_dict['discount'] = i.discount
            data_dict['hsn'] = i.hsn
            data_dict['gst'] = i.gst
            data_dict['taxable_amount'] = i.taxable_amount
            data_dict['tax'] = i.tax
            data_dict['expiry'] = store_medicine[0]['expiry']

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
            'old_credit_sum': old_credit_sum,
            'is_last': is_last,
        }
        return render(request, 'normal_bill/update_direct_estimate.html', context)


def estimate_generate_invoice_number():
    obj, _ = EstimateInvoiceTracker.objects.get_or_create(year=datetime.now().year)
    invoice_number = obj.get_next_invoice_number()
    return invoice_number


@login_required(login_url='/account/user_login/')
def estimate_medicine_order_bill(request, order_type, id):
    if request.method == 'POST':
        form = request.POST
        user_id = request.session['user_id']
        try:
            store = Store.objects.get(user_id=user_id)
            store_id = store.id
        except:
            store_id = 0

        status = 'failed'
        msg = 'Bill Creation failed.'

        medicines = json.loads(request.POST.get('medicines'))
        doctor_id = form.get('doctor_id')
        oder_id = form.get('oder_id')
        invoice_number = estimate_generate_invoice_number()

        subtotal = float(form.get('sub_total'))
        discount = int(form.get('total_discount'))
        shipping_packing = float(form.get('shipping_packing'))
        current = float(form.get('current'))

        discount_amount = subtotal * discount / 100
        after_dis_amount = subtotal - discount_amount + shipping_packing
        after_dis_amount = after_dis_amount - current

        cash = float(form.get('cash'))
        online = float(form.get('online'))

        sgst = form.get('sgst')
        cgst = form.get('cgst')

        obj = EstimateMedicineOrderBillHead.objects.create(order_id_id=oder_id,
                                                           doctor_id=doctor_id,
                                                           store_id=store_id,
                                                           invoice_number=invoice_number,
                                                           sgst=sgst,
                                                           cgst=cgst,
                                                           subtotal=subtotal,
                                                           current=current,
                                                           cash=cash,
                                                           online=online,
                                                           shipping=shipping_packing,
                                                           discount=discount,
                                                           discount_amount=discount_amount,
                                                           pay_amount=after_dis_amount,
                                                           status=1,
                                                           order_type=order_type,
                                                           )
        if obj:
            head_id = obj.id
            for medicine_data in medicines:
                medicine_id = medicine_data['medicine_id']
                record_qty = int(medicine_data['record_qty'])
                sell_qty = int(medicine_data['sell_qty'])
                discount = int(medicine_data['discount'])
                mrp = float(medicine_data['mrp'])
                sale_rate = float(medicine_data['sale_rate'])
                try:
                    hsn = medicine_data['hsn']
                except:
                    hsn = 0

                try:
                    gst = int(medicine_data['gst'])
                except:
                    gst = 0

                try:
                    taxable_amount = float(medicine_data['taxable_amount'])
                except:
                    taxable_amount = 0

                try:
                    tax = float(medicine_data['tax'])
                except:
                    tax = 0
                amount = float(medicine_data['amount'])

                EstimateMedicineOrderBillDetail.objects.create(head_id=head_id,
                                                               medicine_id=medicine_id,
                                                               record_qty=record_qty,
                                                               sell_qty=sell_qty,
                                                               mrp=mrp,
                                                               discount=discount,
                                                               sale_rate=sale_rate,
                                                               hsn=hsn,
                                                               gst=gst,
                                                               taxable_amount=taxable_amount,
                                                               tax=tax,
                                                               amount=amount,
                                                               )
                if sell_qty < record_qty:
                    remaining_qty = int(record_qty) - int(sell_qty)
                    MedicineStore.objects.filter(to_store_id=store_id, medicine_id=medicine_id).update(
                        qty=remaining_qty)
            MedicineOrderBillHead.objects.filter(id=id).update(status=1, estimate_status=1)
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

        user = MedicineOrderBillHead.objects.get(id=id)
        oder_id = user.order_id.id
        invoice_number = user.invoice_number

        cash_online_amount = EstimateMedicineOrderBillHead.objects.filter(doctor_id=user.doctor.id).aggregate(
            total=Sum(
                Coalesce(F('cash'), 0) +
                Coalesce(F('online'), 0) +
                Coalesce(F('extra_cash_amount'), 0) +
                Coalesce(F('extra_online_amount'), 0),
                output_field=DecimalField()
            )
        )['total'] or 0

        total_pay_amount = EstimateMedicineOrderBillHead.objects.filter(doctor_id=user.doctor.id).aggregate(
            total=Sum('pay_amount')
        )['total'] or 0

        old_credit_sum = total_pay_amount - cash_online_amount

        medicine = MedicineOrderBillDetail.objects.filter(head_id=id)
        medicine_list = []
        for i in medicine:
            data_dict = {}
            query = Q(to_store_id=store_id, medicine_id=i.medicine.id)
            store_medicine = MedicineStore.objects.filter(query).values('qty', 'price', 'expiry')
            data_dict['medicine_id'] = i.medicine.id
            data_dict['medicine_name'] = i.medicine.name
            data_dict['order_qty'] = i.order_qty
            data_dict['sell_qty'] = i.sell_qty
            data_dict['discount'] = i.discount
            data_dict['hsn'] = i.hsn
            data_dict['gst'] = i.gst
            data_dict['taxable_amount'] = i.taxable_amount
            data_dict['tax'] = i.tax
            try:
                data_dict['expiry'] = store_medicine[0]['expiry']
            except:
                data_dict['expiry'] = ''

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
            'old_credit_sum': old_credit_sum,
            'invoice_number': invoice_number,
            'oder_id': oder_id,
        }
        if order_type == 1:
            return render(request, 'estimate_bill/estimate_medicine_order_bill_instate.html', context)
        elif order_type == 2:
            return render(request, 'estimate_bill/estimate_medicine_order_bill_other_state.html', context)
        elif order_type == 3:
            return render(request, 'estimate_bill/estimate_medicine_order_bill_of_supply.html', context)
        else:
            return render(request, 'estimate_bill/estimate_medicine_order_bill_of_supply.html', context)


# @login_required(login_url='/account/user_login/')
# def update_estimate_medicine_order_bill(request, order_type, id):
#     if request.method == 'POST':
#         form = request.POST
#         user_id = request.session['user_id']
#         try:
#             store = Store.objects.get(user_id=user_id)
#             store_id = store.id
#         except:
#             store_id = 0
#
#         status = 'failed'
#         msg = 'Estimated Bill updated failed.'
#         medicines = json.loads(request.POST.get('medicines'))
#
#         subtotal = float(form.get('sub_total'))
#         discount1 = int(form.get('total_discount'))
#         shipping_packing = float(form.get('shipping_packing'))
#         current = float(form.get('current'))
#
#         discount_amount = subtotal * discount1 / 100
#         after_dis_amount = subtotal - discount_amount + shipping_packing
#         after_dis_amount = after_dis_amount - current
#
#         cash = float(form.get('cash'))
#         online = float(form.get('online'))
#
#         sgst = form.get('sgst')
#         cgst = form.get('cgst')
#
#         head_id = id
#         medicine_ids = []
#         for medicine_data in medicines:
#             medicine_id = medicine_data['medicine_id']
#             medicine_ids.append(medicine_id)
#             record_qty = int(medicine_data['record_qty'])
#             sell_qty = int(medicine_data['sell_qty'])
#             discount = int(medicine_data['discount'])
#             mrp = float(medicine_data['mrp'])
#             sale_rate = float(medicine_data['sale_rate'])
#             try:
#                 hsn = medicine_data['hsn']
#             except:
#                 hsn = 0
#
#             try:
#                 gst = int(medicine_data['gst'])
#             except:
#                 gst = 0
#
#             try:
#                 taxable_amount = float(medicine_data['taxable_amount'])
#             except:
#                 taxable_amount = 0
#
#             try:
#                 tax = float(medicine_data['tax'])
#             except:
#                 tax = 0
#             amount = float(medicine_data['amount'])
#             query = Q(head_id=head_id, medicine_id=medicine_id)
#             already_obj = EstimateMedicineOrderBillDetail.objects.filter(query)
#             if already_obj:
#                 EstimateMedicineOrderBillDetail.objects.filter(query).update(record_qty=record_qty,
#                                                                              sell_qty=sell_qty,
#                                                                              mrp=mrp,
#                                                                              discount=discount,
#                                                                              sale_rate=sale_rate,
#                                                                              hsn=hsn,
#                                                                              gst=gst,
#                                                                              taxable_amount=taxable_amount,
#                                                                              tax=tax,
#                                                                              amount=amount,
#                                                                              )
#         obj = EstimateMedicineOrderBillHead.objects.filter(id=id).update(store_id=store_id,
#                                                                          sgst=sgst,
#                                                                          cgst=cgst,
#                                                                          subtotal=subtotal,
#                                                                          current=current,
#                                                                          cash=cash,
#                                                                          online=online,
#                                                                          shipping=shipping_packing,
#                                                                          discount=discount1,
#                                                                          discount_amount=discount_amount,
#                                                                          pay_amount=after_dis_amount,
#                                                                          )
#         if obj:
#             EstimateMedicineOrderBillHead.objects.filter(id=id).update(status=1)
#             EstimateMedicineOrderBillDetail.objects.filter(head_id=id).exclude(medicine_id__in=medicine_ids).delete()
#             status = 'success'
#             msg = 'Estimated Bill updated Successfully.'
#
#         context = {
#             'status': status,
#             'msg': msg,
#         }
#         return JsonResponse(context)
#
#     else:
#         user_id = request.session['user_id']
#         try:
#             store = Store.objects.get(user_id=user_id)
#             store_id = store.id
#         except:
#             store_id = 0
#
#         user = EstimateMedicineOrderBillHead.objects.get(id=id)
#
#         is_last = user.id == \
#                   EstimateMedicineOrderBillHead.objects.filter(doctor_id=user.doctor.id).aggregate(Max('id'))['id__max']
#         if is_last:
#             is_last = True
#         else:
#             is_last = False
#
#         cash_online_amount = \
#             EstimateMedicineOrderBillHead.objects.filter(doctor_id=user.doctor.id).exclude(id=id).aggregate(
#                 total=Sum(
#                     Coalesce(F('cash'), 0) +
#                     Coalesce(F('online'), 0) +
#                     Coalesce(F('extra_cash_amount'), 0) +
#                     Coalesce(F('extra_online_amount'), 0),
#                     output_field=DecimalField()
#                 )
#             )['total'] or 0
#
#         total_pay_amount = \
#             EstimateMedicineOrderBillHead.objects.filter(doctor_id=user.doctor.id).exclude(id=id).aggregate(
#                 total=Sum('pay_amount')
#             )['total'] or 0
#
#         old_credit_sum = total_pay_amount - cash_online_amount
#
#         medicine = EstimateMedicineOrderBillDetail.objects.filter(head_id=id)
#         medicine_count = EstimateMedicineOrderBillDetail.objects.filter(head_id=id).count()
#         medicine_list = []
#
#         for i in medicine:
#             data_dict = {}
#             query = Q(to_store_id=store_id, medicine_id=i.medicine.id)
#             store_medicine = MedicineStore.objects.filter(query).values('qty', 'price', 'expiry')
#             data_dict['medicine_id'] = i.medicine.id
#             data_dict['medicine_name'] = i.medicine.name
#             data_dict['order_qty'] = i.order_qty
#             data_dict['sell_qty'] = i.sell_qty
#             data_dict['discount'] = i.discount
#             data_dict['hsn'] = i.hsn
#             data_dict['gst'] = i.gst
#             data_dict['taxable_amount'] = i.taxable_amount
#             data_dict['tax'] = i.tax
#             try:
#                 data_dict['expiry'] = store_medicine[0]['expiry']
#             except:
#                 data_dict['expiry'] = ''
#
#             try:
#                 data_dict['record_qty'] = store_medicine[0]['qty']
#             except:
#                 data_dict['record_qty'] = 0
#             try:
#                 data_dict['mrp'] = store_medicine[0]['price']
#             except:
#                 data_dict['mrp'] = 0
#
#             medicine_list.append(data_dict)
#
#         context = {
#             'id': id,
#             'order_type': order_type,
#             'store_id': store_id,
#             'user': user,
#             'medicine': medicine_list,
#             'old_credit_sum': old_credit_sum,
#             'is_last': is_last,
#         }
#         if order_type == 1:
#             return render(request, 'estimate_bill/update_estimate_medicine_order_bill_instate.html', context)
#         elif order_type == 2:
#             return render(request, 'estimate_bill/update_estimate_medicine_order_bill_other_state.html', context)
#         elif order_type == 3:
#             return render(request, 'estimate_bill/update_estimate_medicine_order_bill_of_supply.html', context)
#         else:
#             return render(request, 'estimate_bill/update_estimate_medicine_order_bill_of_supply.html', context)


@login_required(login_url='/account/user_login/')
def update_estimate_medicine_order_bill(request, order_type, id):
    if request.method == 'POST':
        form = request.POST
        user_id = request.session['user_id']
        try:
            store = Store.objects.get(user_id=user_id)
            store_id = store.id
        except:
            store_id = 0

        status = 'failed'
        msg = 'Estimated Bill updated failed.'
        medicines = json.loads(request.POST.get('medicines'))

        subtotal = float(form.get('sub_total'))
        discount1 = int(form.get('total_discount'))
        shipping_packing = float(form.get('shipping_packing'))
        current = float(form.get('current'))

        discount_amount = subtotal * discount1 / 100
        after_dis_amount = subtotal - discount_amount + shipping_packing
        after_dis_amount = after_dis_amount - current

        cash = float(form.get('cash'))
        online = float(form.get('online'))

        sgst = form.get('sgst')
        cgst = form.get('cgst')

        head_id = id
        medicine_ids = []
        for medicine_data in medicines:
            medicine_id = medicine_data['medicine_id']
            medicine_ids.append(medicine_id)
            record_qty = int(medicine_data['record_qty'])
            sell_qty = int(medicine_data['sell_qty'])
            discount = int(medicine_data['discount'])
            mrp = float(medicine_data['mrp'])
            sale_rate = float(medicine_data['sale_rate'])
            try:
                hsn = medicine_data['hsn']
            except:
                hsn = 0

            try:
                gst = int(medicine_data['gst'])
            except:
                gst = 0

            try:
                taxable_amount = float(medicine_data['taxable_amount'])
            except:
                taxable_amount = 0

            try:
                tax = float(medicine_data['tax'])
            except:
                tax = 0
            amount = float(medicine_data['amount'])
            query = Q(head_id=head_id, medicine_id=medicine_id)
            already_obj = DirectEstimateDetail.objects.filter(query)
            if already_obj:
                DirectEstimateDetail.objects.filter(query).update(record_qty=record_qty,
                                                                  sell_qty=sell_qty,
                                                                  mrp=mrp,
                                                                  discount=discount,
                                                                  sale_rate=sale_rate,
                                                                  hsn=hsn,
                                                                  gst=gst,
                                                                  taxable_amount=taxable_amount,
                                                                  tax=tax,
                                                                  amount=amount,
                                                                  )
        obj = DirectEstimateHead.objects.filter(id=id).update(store_id=store_id,
                                                              sgst=sgst,
                                                              cgst=cgst,
                                                              subtotal=subtotal,
                                                              current=current,
                                                              cash=cash,
                                                              online=online,
                                                              shipping=shipping_packing,
                                                              discount=discount1,
                                                              discount_amount=discount_amount,
                                                              pay_amount=after_dis_amount,
                                                              )
        if obj:
            DirectEstimateHead.objects.filter(id=id).update(status=1)
            DirectEstimateDetail.objects.filter(head_id=id).exclude(medicine_id__in=medicine_ids).delete()
            status = 'success'
            msg = 'Estimated Bill updated Successfully.'

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

        user = DirectEstimateHead.objects.get(id=id)

        is_last = user.id == \
                  DirectEstimateHead.objects.filter(doctor_id=user.doctor.id).aggregate(Max('id'))['id__max']
        if is_last:
            is_last = True
        else:
            is_last = False

        cash_online_amount = \
            DirectEstimateHead.objects.filter(doctor_id=user.doctor.id).exclude(id=id).aggregate(
                total=Sum(
                    Coalesce(F('cash'), 0) +
                    Coalesce(F('online'), 0) +
                    Coalesce(F('extra_cash_amount'), 0) +
                    Coalesce(F('extra_online_amount'), 0),
                    output_field=DecimalField()
                )
            )['total'] or 0

        total_pay_amount = \
            DirectEstimateHead.objects.filter(doctor_id=user.doctor.id).exclude(id=id).aggregate(
                total=Sum('pay_amount')
            )['total'] or 0

        old_credit_sum = total_pay_amount - cash_online_amount

        medicine = DirectEstimateDetail.objects.filter(head_id=id)
        medicine_count = DirectEstimateDetail.objects.filter(head_id=id).count()
        medicine_list = []

        for i in medicine:
            data_dict = {}
            query = Q(to_store_id=store_id, medicine_id=i.medicine.id)
            store_medicine = MedicineStore.objects.filter(query).values('qty', 'price', 'expiry')
            data_dict['medicine_id'] = i.medicine.id
            data_dict['medicine_name'] = i.medicine.name
            data_dict['order_qty'] = i.order_qty
            data_dict['sell_qty'] = i.sell_qty
            data_dict['discount'] = i.discount
            data_dict['hsn'] = i.hsn
            data_dict['gst'] = i.gst
            data_dict['taxable_amount'] = i.taxable_amount
            data_dict['tax'] = i.tax
            try:
                data_dict['expiry'] = store_medicine[0]['expiry']
            except:
                data_dict['expiry'] = ''

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
            'old_credit_sum': old_credit_sum,
            'is_last': is_last,
        }
        return render(request, 'estimate_bill/update_estimate_medicine_order_bill_of_supply.html', context)


@login_required(login_url='/account/user_login/')
def view_normal(request, id):
    user_id = request.session['user_id']
    try:
        store = Store.objects.get(user_id=user_id)
        store_id = store.id
    except:
        store_id = 0

    pay_detail = PaymentDetail.objects.filter()
    try:
        user = MedicineOrderBillHead.objects.get(order_id_id=id)
    except:
        return redirect('/my_order/my_medicine_ordered_list/')
    order_type = user.order_type
    old_credit_sum = \
        MedicineOrderBillHead.objects.filter(doctor_id=user.doctor.id).exclude(order_id_id=id).aggregate(
            Sum('old_credit'))[
            'old_credit__sum'] or 0
    medicine = MedicineOrderBillDetail.objects.filter(head_id=user.id)
    medicine_list = []

    for i in medicine:
        data_dict = {}
        data_dict['medicine_id'] = i.medicine.id
        data_dict['medicine_name'] = i.medicine.name
        data_dict['record_qty'] = i.record_qty
        data_dict['order_qty'] = i.order_qty
        data_dict['sell_qty'] = i.sell_qty
        data_dict['mrp'] = i.mrp
        data_dict['discount'] = i.discount
        data_dict['hsn'] = i.hsn
        data_dict['gst'] = i.gst
        data_dict['taxable_amount'] = i.taxable_amount
        data_dict['tax'] = i.tax
        medicine_list.append(data_dict)

    context = {
        'id': id,
        'order_type': order_type,
        'store_id': store_id,
        'user': user,
        'medicine': medicine_list,
        'old_credit_sum': old_credit_sum,
        'pay_detail': pay_detail[0],
    }
    if order_type == 1:
        return render(request, 'normal_bill/view_normal_instate.html', context)
    elif order_type == 2:
        return render(request, 'normal_bill/view_normal_other_state.html', context)
    elif order_type == 3:
        return render(request, 'normal_bill/view_normal_bill_of_supply.html', context)
    else:
        return render(request, 'normal_bill/view_normal_bill_of_supply.html', context)


@login_required(login_url='/account/user_login/')
def view_estimate(request, id):
    user_id = request.session['user_id']
    try:
        store = Store.objects.get(user_id=user_id)
        store_id = store.id
    except:
        store_id = 0
    try:
        user = EstimateMedicineOrderBillHead.objects.get(order_id_id=id)
    except:
        return redirect('/my_order/my_medicine_ordered_list/')
    pay_detail = PaymentDetail.objects.filter()
    order_type = user.order_type
    old_credit_sum = \
        EstimateMedicineOrderBillHead.objects.filter(doctor_id=user.doctor.id).exclude(order_id_id=id).aggregate(
            Sum('old_credit'))[
            'old_credit__sum'] or 0
    medicine = EstimateMedicineOrderBillDetail.objects.filter(head_id=user.id)
    medicine_list = []

    for i in medicine:
        data_dict = {}
        data_dict['medicine_id'] = i.medicine.id
        data_dict['medicine_name'] = i.medicine.name
        data_dict['record_qty'] = i.record_qty
        data_dict['order_qty'] = i.order_qty
        data_dict['sell_qty'] = i.sell_qty
        data_dict['mrp'] = i.mrp
        data_dict['discount'] = i.discount
        data_dict['hsn'] = i.hsn
        data_dict['gst'] = i.gst
        data_dict['taxable_amount'] = i.taxable_amount
        data_dict['tax'] = i.tax

        medicine_list.append(data_dict)

    context = {
        'id': id,
        'order_type': order_type,
        'store_id': store_id,
        'user': user,
        'medicine': medicine_list,
        'old_credit_sum': old_credit_sum,
        'pay_detail': pay_detail[0],
    }
    if order_type == 1:
        return render(request, 'estimate_bill/view_estimate_instate.html', context)
    elif order_type == 2:
        return render(request, 'estimate_bill/view_estimate_other_state.html', context)
    elif order_type == 3:
        return render(request, 'estimate_bill/view_estimate_bill_of_supply.html', context)
    else:
        return render(request, 'estimate_bill/view_estimate_bill_of_supply.html', context)


def view_normal_invoice(request, id):
    user_id = request.session['user_id']
    try:
        store = Store.objects.get(user_id=user_id)
        store_id = store.id
    except:
        store_id = 0
    try:
        user = MedicineOrderBillHead.objects.get(id=id)
    except:
        return redirect('/my_order/my_medicine_ordered_list/')

    order_type = user.order_type
    invoice_number = user.invoice_number
    cash_online_amount = MedicineOrderBillHead.objects.filter(doctor_id=user.doctor.id).exclude(id=id).aggregate(
        total=Sum(
            Coalesce(F('cash'), 0) +
            Coalesce(F('online'), 0) +
            Coalesce(F('extra_cash_amount'), 0) +
            Coalesce(F('extra_online_amount'), 0),
            output_field=DecimalField()
        )
    )['total'] or 0

    total_pay_amount = MedicineOrderBillHead.objects.filter(doctor_id=user.doctor.id).exclude(id=id).aggregate(
        total=Sum('pay_amount')
    )['total'] or 0

    old_credit_sum = total_pay_amount - cash_online_amount

    pay_amount = user.pay_amount
    cash = user.cash
    online = user.online

    remaining_amount = pay_amount - (cash + online) + old_credit_sum
    current = user.current

    medicine = MedicineOrderBillDetail.objects.filter(head_id=user.id)
    gst_per = MedicineOrderBillDetail.objects.filter(head_id=user.id).values_list('gst', flat=True).distinct()

    total_taxable_by_gst_list = []
    grand_sub_total = 0
    grand_discount_total = 0
    grand_taxable_amount_total = 0
    grand_sgst_and_cgst_total = 0
    grand_tax_total = 0
    for gst in gst_per:
        # Total taxable amounts
        total_taxable = MedicineOrderBillDetail.objects.filter(
            head_id=user.id, gst=gst
        ).aggregate(total_taxable=Sum('taxable_amount'))['total_taxable'] or 0
        grand_taxable_amount_total += total_taxable

        # Sub totals
        medicine_sub_totals = MedicineOrderBillDetail.objects.filter(
            head_id=user.id, gst=gst
        ).annotate(
            total=F('sell_qty') * F('mrp'),
            discount_amount=ExpressionWrapper(
                (F('sell_qty') * F('mrp') * F('discount') / 100),
                output_field=FloatField()
            )
        )

        # Sub total calculation
        sub_total = medicine_sub_totals.aggregate(grand_total=Sum('total'))['grand_total'] or 0
        grand_sub_total += sub_total

        # Discount total calculation
        discount_total = medicine_sub_totals.aggregate(grand_discount=Sum('discount_amount'))['grand_discount'] or 0
        grand_discount_total += discount_total

        tax = MedicineOrderBillDetail.objects.filter(
            head_id=user.id, gst=gst
        ).aggregate(tax=Sum('tax'))['tax'] or 0
        grand_tax_total += tax

        if order_type == 1:
            sgst_and_cgst = tax / 2
        elif order_type == 2:
            sgst_and_cgst = tax
        else:
            sgst_and_cgst = tax

        grand_sgst_and_cgst_total += sgst_and_cgst
        total_taxable_by_gst_list.append({
            'gst': gst,
            'taxable_amount': total_taxable,
            'sub_total': sub_total,
            'discount': discount_total,
            'tax': tax,
            'sgst_and_cgst': sgst_and_cgst,
        })

    total_discounted_price = 0
    for item in medicine:
        if item.mrp and item.discount and item.sell_qty:  # Ensure values are not None
            discount_amount = (item.mrp * item.discount) / 100  # Calculate discount amount per unit
            discounted_price_per_unit = discount_amount  # Calculate discounted price per unit
            total_price_for_item = discounted_price_per_unit * item.sell_qty  # Multiply by sell quantity
            total_discounted_price += total_price_for_item  # Add to total discounted price

    subtotal_amount = medicine.aggregate(total_amount=Sum(F('sell_qty') * F('mrp')))['total_amount'] or 0
    total_taxable_amount = medicine.aggregate(total_taxable=Sum('taxable_amount'))['total_taxable'] or 0

    context = {
        'id': id,
        'order_type': order_type,
        'store_id': store_id,
        'user': user,
        'medicine': medicine,
        'total_taxable_by_gst': total_taxable_by_gst_list,
        'total_discounted_price': total_discounted_price,
        'subtotal_amount': subtotal_amount,
        'total_taxable_amount': total_taxable_amount,

        'grand_sub_total': grand_sub_total,
        'grand_discount_total': grand_discount_total,
        'grand_taxable_amount_total': grand_taxable_amount_total,
        'grand_sgst_and_cgst_total': grand_sgst_and_cgst_total,
        'grand_tax_total': grand_tax_total,

        'remaining_amount': remaining_amount,
        'current': current,
        'old_credit_sum': old_credit_sum,
        'invoice_number': invoice_number,
    }

    if order_type == 1:
        return render(request, 'invoice/normal_invoice/normal_invoice_instate.html', context)
    elif order_type == 2:
        return render(request, 'invoice/normal_invoice/normal_invoice_other_state.html', context)
    elif order_type == 3:
        return render(request, 'invoice/normal_invoice/normal_invoice_bill_of_supply.html', context)
    else:
        return render(request, 'invoice/normal_invoice/normal_invoice_bill_of_supply.html', context)


def final_bill_invoice(request, id):
    user_id = request.session['user_id']
    try:
        store = Store.objects.get(user_id=user_id)
        store_id = store.id
    except:
        store_id = 0
    try:
        user = MedicineUnregisteredOrderBillHead.objects.get(head_id=id)
    except:
        return redirect('/bill/normal_order_bill_list/')

    order_type = user.order_type
    invoice_number = user.invoice_number
    cash_online_amount = \
        MedicineUnregisteredOrderBillHead.objects.filter(doctor_id=user.doctor.id).exclude(head_id=id).aggregate(
            total=Sum(
                Coalesce(F('cash'), 0) +
                Coalesce(F('online'), 0) +
                Coalesce(F('extra_cash_amount'), 0) +
                Coalesce(F('extra_online_amount'), 0),
                output_field=DecimalField()
            )
        )['total'] or 0

    total_pay_amount = \
        MedicineUnregisteredOrderBillHead.objects.filter(doctor_id=user.doctor.id).exclude(head_id=id).aggregate(
            total=Sum('pay_amount')
        )['total'] or 0

    old_credit_sum = total_pay_amount - cash_online_amount

    pay_amount = user.pay_amount
    cash = user.cash
    online = user.online

    remaining_amount = pay_amount - (cash + online) + old_credit_sum
    current = user.current

    medicine = MedicineUnregisteredOrderBillDetail.objects.filter(head_id=user.id)
    gst_per = MedicineUnregisteredOrderBillDetail.objects.filter(head_id=user.id).values_list('gst',
                                                                                              flat=True).distinct()

    total_taxable_by_gst_list = []
    grand_sub_total = 0
    grand_discount_total = 0
    grand_taxable_amount_total = 0
    grand_sgst_and_cgst_total = 0
    grand_tax_total = 0
    for gst in gst_per:
        # Total taxable amounts
        total_taxable = MedicineUnregisteredOrderBillDetail.objects.filter(
            head_id=user.id, gst=gst
        ).aggregate(total_taxable=Sum('taxable_amount'))['total_taxable'] or 0
        grand_taxable_amount_total += total_taxable

        # Sub totals
        medicine_sub_totals = MedicineUnregisteredOrderBillDetail.objects.filter(
            head_id=user.id, gst=gst
        ).annotate(
            total=F('sell_qty') * F('mrp'),
            discount_amount=ExpressionWrapper(
                (F('sell_qty') * F('mrp') * F('discount') / 100),
                output_field=FloatField()
            )
        )

        # Sub total calculation
        sub_total = medicine_sub_totals.aggregate(grand_total=Sum('total'))['grand_total'] or 0
        grand_sub_total += sub_total

        # Discount total calculation
        discount_total = medicine_sub_totals.aggregate(grand_discount=Sum('discount_amount'))['grand_discount'] or 0
        grand_discount_total += discount_total

        tax = MedicineUnregisteredOrderBillDetail.objects.filter(
            head_id=user.id, gst=gst
        ).aggregate(tax=Sum('tax'))['tax'] or 0
        grand_tax_total += tax

        if order_type == 1:
            sgst_and_cgst = tax / 2
        elif order_type == 2:
            sgst_and_cgst = tax
        else:
            sgst_and_cgst = tax

        grand_sgst_and_cgst_total += sgst_and_cgst
        total_taxable_by_gst_list.append({
            'gst': gst,
            'taxable_amount': total_taxable,
            'sub_total': sub_total,
            'discount': discount_total,
            'tax': tax,
            'sgst_and_cgst': sgst_and_cgst,
        })

    total_discounted_price = 0
    for item in medicine:
        if item.mrp and item.discount and item.sell_qty:  # Ensure values are not None
            discount_amount = (item.mrp * item.discount) / 100  # Calculate discount amount per unit
            discounted_price_per_unit = discount_amount  # Calculate discounted price per unit
            total_price_for_item = discounted_price_per_unit * item.sell_qty  # Multiply by sell quantity
            total_discounted_price += total_price_for_item  # Add to total discounted price

    subtotal_amount = medicine.aggregate(total_amount=Sum(F('sell_qty') * F('mrp')))['total_amount'] or 0
    total_taxable_amount = medicine.aggregate(total_taxable=Sum('taxable_amount'))['total_taxable'] or 0

    context = {
        'id': id,
        'order_type': order_type,
        'store_id': store_id,
        'user': user,
        'medicine': medicine,
        'total_taxable_by_gst': total_taxable_by_gst_list,
        'total_discounted_price': total_discounted_price,
        'subtotal_amount': subtotal_amount,
        'total_taxable_amount': total_taxable_amount,

        'grand_sub_total': grand_sub_total,
        'grand_discount_total': grand_discount_total,
        'grand_taxable_amount_total': grand_taxable_amount_total,
        'grand_sgst_and_cgst_total': grand_sgst_and_cgst_total,
        'grand_tax_total': grand_tax_total,

        'remaining_amount': remaining_amount,
        'current': current,
        'old_credit_sum': old_credit_sum,
        'invoice_number': invoice_number,
    }

    if order_type == 1:
        return render(request, 'invoice/normal_final_invoive/normal_invoice_instate.html', context)
    elif order_type == 2:
        return render(request, 'invoice/normal_final_invoive/normal_invoice_other_state.html', context)
    elif order_type == 3:
        return render(request, 'invoice/normal_final_invoive/normal_invoice_bill_of_supply.html', context)
    else:
        return render(request, 'invoice/normal_final_invoive/normal_invoice_bill_of_supply.html', context)


def view_normal_invoice_doctor(request, id):
    user_id = request.session['user_id']
    try:
        store = Store.objects.get(user_id=user_id)
        store_id = store.id
    except:
        store_id = 0
    try:
        user = MedicineOrderBillHead.objects.get(order_id_id=id)
    except:
        return redirect('/my_order/my_medicine_ordered_list/')

    order_type = user.order_type

    cash_online_amount = \
        MedicineOrderBillHead.objects.filter(doctor_id=user.doctor.id).exclude(order_id_id=id).aggregate(
            total=Sum(
                Coalesce(F('cash'), 0) +
                Coalesce(F('online'), 0) +
                Coalesce(F('extra_cash_amount'), 0) +
                Coalesce(F('extra_online_amount'), 0),
                output_field=DecimalField()
            )
        )['total'] or 0

    total_pay_amount = MedicineOrderBillHead.objects.filter(doctor_id=user.doctor.id).exclude(order_id_id=id).aggregate(
        total=Sum('pay_amount')
    )['total'] or 0

    old_credit_sum = total_pay_amount - cash_online_amount
    pay_amount = user.pay_amount
    cash = user.cash
    online = user.online

    remaining_amount = pay_amount - (cash + online) + old_credit_sum
    current = user.current
    medicine = MedicineOrderBillDetail.objects.filter(head_id=user.id)
    gst_per = MedicineOrderBillDetail.objects.filter(head_id=user.id).values_list('gst', flat=True).distinct()

    total_taxable_by_gst_list = []
    grand_sub_total = 0
    grand_discount_total = 0
    grand_taxable_amount_total = 0
    grand_sgst_and_cgst_total = 0
    grand_tax_total = 0
    for gst in gst_per:
        # Total taxable amounts
        total_taxable = MedicineOrderBillDetail.objects.filter(
            head_id=user.id, gst=gst
        ).aggregate(total_taxable=Sum('taxable_amount'))['total_taxable'] or 0
        grand_taxable_amount_total += total_taxable

        # Sub totals
        medicine_sub_totals = MedicineOrderBillDetail.objects.filter(
            head_id=user.id, gst=gst
        ).annotate(
            total=F('sell_qty') * F('mrp'),
            discount_amount=ExpressionWrapper(
                (F('sell_qty') * F('mrp') * F('discount') / 100),
                output_field=FloatField()
            )
        )

        # Sub total calculation
        sub_total = medicine_sub_totals.aggregate(grand_total=Sum('total'))['grand_total'] or 0
        grand_sub_total += sub_total

        # Discount total calculation
        discount_total = medicine_sub_totals.aggregate(grand_discount=Sum('discount_amount'))['grand_discount'] or 0
        grand_discount_total += discount_total

        tax = MedicineOrderBillDetail.objects.filter(
            head_id=user.id, gst=gst
        ).aggregate(tax=Sum('tax'))['tax'] or 0
        grand_tax_total += tax
        sgst_and_cgst = tax / 2
        grand_sgst_and_cgst_total += sgst_and_cgst
        total_taxable_by_gst_list.append({
            'gst': gst,
            'taxable_amount': total_taxable,
            'sub_total': sub_total,
            'discount': discount_total,
            'tax': tax,
            'sgst_and_cgst': sgst_and_cgst,
        })

    total_discounted_price = 0
    for item in medicine:
        if item.mrp and item.discount and item.sell_qty:  # Ensure values are not None
            discount_amount = (item.mrp * item.discount) / 100  # Calculate discount amount per unit
            discounted_price_per_unit = discount_amount  # Calculate discounted price per unit
            total_price_for_item = discounted_price_per_unit * item.sell_qty  # Multiply by sell quantity
            total_discounted_price += total_price_for_item  # Add to total discounted price

    subtotal_amount = medicine.aggregate(total_amount=Sum(F('sell_qty') * F('mrp')))['total_amount'] or 0
    total_taxable_amount = medicine.aggregate(total_taxable=Sum('taxable_amount'))['total_taxable'] or 0

    context = {
        'id': id,
        'order_type': order_type,
        'store_id': store_id,
        'user': user,
        'medicine': medicine,
        'old_credit_sum': old_credit_sum,
        'total_taxable_by_gst': total_taxable_by_gst_list,
        'total_discounted_price': total_discounted_price,
        'subtotal_amount': subtotal_amount,
        'total_taxable_amount': total_taxable_amount,

        'grand_sub_total': grand_sub_total,
        'grand_discount_total': grand_discount_total,
        'grand_taxable_amount_total': grand_taxable_amount_total,
        'grand_sgst_and_cgst_total': grand_sgst_and_cgst_total,
        'grand_tax_total': grand_tax_total,

        'current': current,
        'pay_amount': pay_amount,
        'remaining_amount': remaining_amount,
    }
    if order_type == 1:
        return render(request, 'invoice/normal_invoice/normal_invoice_instate.html', context)
    elif order_type == 2:
        return render(request, 'invoice/normal_invoice/normal_invoice_other_state.html', context)
    elif order_type == 3:
        return render(request, 'invoice/normal_invoice/normal_invoice_bill_of_supply.html', context)
    else:
        return render(request, 'invoice/normal_invoice/normal_invoice_bill_of_supply.html', context)


# def view_estimate_invoice(request, id):
#     user_id = request.session['user_id']
#     try:
#         store = Store.objects.get(user_id=user_id)
#         store_id = store.id
#     except:
#         store_id = 0
#     try:
#         user = EstimateMedicineOrderBillHead.objects.get(id=id)
#     except:
#         return redirect('/my_order/my_medicine_ordered_list/')
#     order_type = user.order_type
#
#     cash_online_amount = \
#         EstimateMedicineOrderBillHead.objects.filter(doctor_id=user.doctor.id).exclude(id=id).aggregate(
#             total=Sum(
#                 Coalesce(F('cash'), 0) +
#                 Coalesce(F('online'), 0) +
#                 Coalesce(F('extra_cash_amount'), 0) +
#                 Coalesce(F('extra_online_amount'), 0),
#                 output_field=DecimalField()
#             )
#         )['total'] or 0
#
#     total_pay_amount = EstimateMedicineOrderBillHead.objects.filter(doctor_id=user.doctor.id).exclude(id=id).aggregate(
#         total=Sum('pay_amount')
#     )['total'] or 0
#
#     old_credit_sum = total_pay_amount - cash_online_amount
#     pay_amount = user.pay_amount
#     cash = user.cash
#     online = user.online
#     total_amt = user.subtotal - user.discount_amount
#
#     remaining_amount = pay_amount - (cash + online) + old_credit_sum
#
#     current = user.current
#
#     medicine = EstimateMedicineOrderBillDetail.objects.filter(head_id=user.id)
#
#     gst_per = EstimateMedicineOrderBillDetail.objects.filter(head_id=user.id).values_list('gst', flat=True).distinct()
#
#     total_taxable_by_gst_list = []
#     grand_sub_total = 0
#     grand_discount_total = 0
#     grand_taxable_amount_total = 0
#     grand_sgst_and_cgst_total = 0
#     grand_tax_total = 0
#
#     for gst in gst_per:
#         # Total taxable amounts
#         total_taxable = EstimateMedicineOrderBillDetail.objects.filter(
#             head_id=user.id, gst=gst
#         ).aggregate(total_taxable=Sum('taxable_amount'))['total_taxable'] or 0
#         grand_taxable_amount_total += total_taxable
#
#         # Sub totals
#         medicine_sub_totals = EstimateMedicineOrderBillDetail.objects.filter(
#             head_id=user.id, gst=gst
#         ).annotate(
#             total=F('sell_qty') * F('mrp'),
#             discount_amount=ExpressionWrapper(
#                 (F('sell_qty') * F('mrp') * F('discount') / 100),
#                 output_field=FloatField()
#             )
#         )
#
#         # Sub total calculation
#         sub_total = medicine_sub_totals.aggregate(grand_total=Sum('total'))['grand_total'] or 0
#         grand_sub_total += sub_total
#
#         # Discount total calculation
#         discount_total = medicine_sub_totals.aggregate(grand_discount=Sum('discount_amount'))['grand_discount'] or 0
#         grand_discount_total += discount_total
#
#         tax = EstimateMedicineOrderBillDetail.objects.filter(
#             head_id=user.id, gst=gst
#         ).aggregate(tax=Sum('tax'))['tax'] or 0
#         grand_tax_total += tax
#         sgst_and_cgst = tax / 2
#         grand_sgst_and_cgst_total += sgst_and_cgst
#         total_taxable_by_gst_list.append({
#             'gst': gst,
#             'taxable_amount': total_taxable,
#             'sub_total': sub_total,
#             'discount': discount_total,
#             'tax': tax,
#             'sgst_and_cgst': sgst_and_cgst,
#         })
#
#     total_discounted_price = 0
#     for item in medicine:
#         if item.mrp and item.discount and item.sell_qty:  # Ensure values are not None
#             discount_amount = (item.mrp * item.discount) / 100  # Calculate discount amount per unit
#             discounted_price_per_unit = discount_amount  # Calculate discounted price per unit
#             total_price_for_item = discounted_price_per_unit * item.sell_qty  # Multiply by sell quantity
#             total_discounted_price += total_price_for_item  # Add to total discounted price
#
#     subtotal_amount = medicine.aggregate(total_amount=Sum(F('sell_qty') * F('mrp')))['total_amount'] or 0
#     total_taxable_amount = medicine.aggregate(total_taxable=Sum('taxable_amount'))['total_taxable'] or 0
#
#     context = {
#         'id': id,
#         'order_type': order_type,
#         'store_id': store_id,
#         'user': user,
#         'medicine': medicine,
#         'old_credit_sum': old_credit_sum,
#         'total_taxable_by_gst': total_taxable_by_gst_list,
#         'total_discounted_price': total_discounted_price,
#         'subtotal_amount': subtotal_amount,
#         'total_taxable_amount': total_taxable_amount,
#
#         'grand_sub_total': grand_sub_total,
#         'grand_discount_total': grand_discount_total,
#         'grand_taxable_amount_total': grand_taxable_amount_total,
#         'grand_sgst_and_cgst_total': grand_sgst_and_cgst_total,
#         'grand_tax_total': grand_tax_total,
#
#         'current': current,
#         'pay_amount': pay_amount,
#         'remaining_amount': remaining_amount,
#         'total_amt': total_amt,
#     }
#     if order_type == 1:
#         return render(request, 'invoice/estimate_invoice/estimate_invoice_instate.html', context)
#     elif order_type == 2:
#         return render(request, 'invoice/estimate_invoice/estimate_invoice_other_state.html', context)
#     elif order_type == 3:
#         return render(request, 'invoice/estimate_invoice/estimate_invoice_bill_of_supply.html', context)
#     else:
#         return render(request, 'invoice/estimate_invoice/estimate_invoice_bill_of_supply.html', context)


def view_estimate_invoice(request, id):
    user_id = request.session['user_id']
    try:
        store = Store.objects.get(user_id=user_id)
        store_id = store.id
    except:
        store_id = 0
    try:
        user = DirectEstimateHead.objects.get(id=id)
    except:
        return redirect('/my_order/my_medicine_ordered_list/')
    order_type = user.order_type

    cash_online_amount = \
        DirectEstimateHead.objects.filter(doctor_id=user.doctor.id).exclude(id=id).aggregate(
            total=Sum(
                Coalesce(F('cash'), 0) +
                Coalesce(F('online'), 0) +
                Coalesce(F('extra_cash_amount'), 0) +
                Coalesce(F('extra_online_amount'), 0),
                output_field=DecimalField()
            )
        )['total'] or 0

    total_pay_amount = DirectEstimateHead.objects.filter(doctor_id=user.doctor.id).exclude(id=id).aggregate(
        total=Sum('pay_amount')
    )['total'] or 0

    old_credit_sum = total_pay_amount - cash_online_amount
    pay_amount = user.pay_amount
    cash = user.cash
    online = user.online
    total_amt = user.subtotal - user.discount_amount

    remaining_amount = pay_amount - (cash + online) + old_credit_sum

    current = user.current

    medicine = DirectEstimateDetail.objects.filter(head_id=user.id)

    gst_per = DirectEstimateDetail.objects.filter(head_id=user.id).values_list('gst', flat=True).distinct()

    total_taxable_by_gst_list = []
    grand_sub_total = 0
    grand_discount_total = 0
    grand_taxable_amount_total = 0
    grand_sgst_and_cgst_total = 0
    grand_tax_total = 0

    for gst in gst_per:
        # Total taxable amounts
        total_taxable = DirectEstimateDetail.objects.filter(
            head_id=user.id, gst=gst
        ).aggregate(total_taxable=Sum('taxable_amount'))['total_taxable'] or 0
        grand_taxable_amount_total += total_taxable

        # Sub totals
        medicine_sub_totals = DirectEstimateDetail.objects.filter(
            head_id=user.id, gst=gst
        ).annotate(
            total=F('sell_qty') * F('mrp'),
            discount_amount=ExpressionWrapper(
                (F('sell_qty') * F('mrp') * F('discount') / 100),
                output_field=FloatField()
            )
        )

        # Sub total calculation
        sub_total = medicine_sub_totals.aggregate(grand_total=Sum('total'))['grand_total'] or 0
        grand_sub_total += sub_total

        # Discount total calculation
        discount_total = medicine_sub_totals.aggregate(grand_discount=Sum('discount_amount'))['grand_discount'] or 0
        grand_discount_total += discount_total

        tax = DirectEstimateDetail.objects.filter(
            head_id=user.id, gst=gst
        ).aggregate(tax=Sum('tax'))['tax'] or 0
        grand_tax_total += tax
        sgst_and_cgst = tax / 2
        grand_sgst_and_cgst_total += sgst_and_cgst
        total_taxable_by_gst_list.append({
            'gst': gst,
            'taxable_amount': total_taxable,
            'sub_total': sub_total,
            'discount': discount_total,
            'tax': tax,
            'sgst_and_cgst': sgst_and_cgst,
        })

    total_discounted_price = 0
    for item in medicine:
        if item.mrp and item.discount and item.sell_qty:  # Ensure values are not None
            discount_amount = (item.mrp * item.discount) / 100  # Calculate discount amount per unit
            discounted_price_per_unit = discount_amount  # Calculate discounted price per unit
            total_price_for_item = discounted_price_per_unit * item.sell_qty  # Multiply by sell quantity
            total_discounted_price += total_price_for_item  # Add to total discounted price

    subtotal_amount = medicine.aggregate(total_amount=Sum(F('sell_qty') * F('mrp')))['total_amount'] or 0
    total_taxable_amount = medicine.aggregate(total_taxable=Sum('taxable_amount'))['total_taxable'] or 0

    context = {
        'id': id,
        'order_type': order_type,
        'store_id': store_id,
        'user': user,
        'medicine': medicine,
        'old_credit_sum': old_credit_sum,
        'total_taxable_by_gst': total_taxable_by_gst_list,
        'total_discounted_price': total_discounted_price,
        'subtotal_amount': subtotal_amount,
        'total_taxable_amount': total_taxable_amount,

        'grand_sub_total': grand_sub_total,
        'grand_discount_total': grand_discount_total,
        'grand_taxable_amount_total': grand_taxable_amount_total,
        'grand_sgst_and_cgst_total': grand_sgst_and_cgst_total,
        'grand_tax_total': grand_tax_total,

        'current': current,
        'pay_amount': pay_amount,
        'remaining_amount': remaining_amount,
        'total_amt': total_amt,
    }
    return render(request, 'invoice/estimate_invoice/estimate_invoice_bill_of_supply.html', context)


def add_extra_amount(request, id):
    if request.method == 'POST':
        form = request.POST
        cash_amount = form.get('cash_amount')
        online_amount = form.get('online_amount')
        amount_remark = form.get('amount_remark')

        if cash_amount:
            cash_amount = Decimal(cash_amount)
        else:
            cash_amount = 0

        if online_amount:
            online_amount = Decimal(online_amount)
        else:
            online_amount = 0

        record = MedicineOrderBillHead.objects.filter(id=id)
        if record:
            pre_cash = record[0].cash
            pre_online = record[0].online

            extra_cash = pre_cash + cash_amount
            extra_online = record[0].online + online_amount
            MedicineOrderBillHead.objects.filter(id=id).update(extra_cash_amount=cash_amount,
                                                               extra_online_amount=online_amount,
                                                               )

            status = 'success'

            context = {
                'status': status,
                'msg': 'Extra amount added successfully.',
            }
            return JsonResponse(context)


def estimate_add_extra_amount(request, id):
    if request.method == 'POST':
        form = request.POST
        cash_amount = form.get('cash_amount')
        online_amount = form.get('online_amount')
        amount_remark = form.get('amount_remark')

        if cash_amount:
            cash_amount = Decimal(cash_amount)
        else:
            cash_amount = 0

        if online_amount:
            online_amount = Decimal(online_amount)
        else:
            online_amount = 0

        record = EstimateMedicineOrderBillHead.objects.filter(id=id)
        if record:
            pre_cash = record[0].cash
            pre_online = record[0].online

            extra_cash = pre_cash + cash_amount
            extra_online = record[0].online + online_amount

            EstimateMedicineOrderBillHead.objects.filter(id=id).update(extra_cash_amount=cash_amount,
                                                                       extra_online_amount=online_amount,
                                                                       )

            status = 'success'

            context = {
                'status': status,
                'msg': 'Extra amount added successfully.',
            }
            return JsonResponse(context)


def delivery_detail(request, id):
    if request.method == 'POST':
        form = request.POST
        track_id = form.get('track_id')
        status_id = form.get('status_id')
        obj = MedicineOrderBillHead.objects.filter(id=id).update(delivery_status_id=status_id,
                                                                 track_id=track_id)

        if obj:
            status = 'success'
            msg = 'Data saved successfully.'
        else:
            status = 'failed'
            msg = 'Data not saved.'

        context = {
            'status': status,
            'msg': msg,
        }
        return JsonResponse(context)

    else:
        delivery = MedicineOrderBillHead.objects.get(id=id)
        context = {
            'id': id,
            'delivery': delivery,
        }
        return render(request, 'delivery_detail.html', context)


def delivery_detail_doctor(request, id):
    delivery = MedicineOrderBillHead.objects.get(order_id_id=id)
    context = {
        'id': id,
        'delivery': delivery,
    }
    return render(request, 'delivery_detail_doctor.html', context)
