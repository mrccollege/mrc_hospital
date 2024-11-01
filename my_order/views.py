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

from my_order.models import MedicineOrderBillHead, MedicineOrderBillDetail

from my_order.models import EstimateMedicineOrderBillHead, EstimateMedicineOrderBillDetail
from django.db.models import Sum


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
        invoice_number = datetime.now().strftime("%Y%d%H%M%S")
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
        for i in medicine:
            print(i.recom_to_doctor, '=============medicine')
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
        return render(request, 'update_medicine_order_bill_instate.html', context)


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

        medicines = json.loads(request.POST.get('medicines'))
        invoice_number = form.get('invoice_number')
        doctor_id = form.get('doctor_id')
        subtotal = float(form.get('sub_total'))
        sgst = form.get('sgst')
        cgst = form.get('cgst')
        cash = float(form.get('cash'))
        online = float(form.get('online'))
        shipping_packing = int(form.get('shipping_packing'))
        discount = int(form.get('total_discount'))
        total = float(form.get('total'))
        new_credit = float(form.get('new_credit'))

        obj = MedicineOrderBillHead.objects.create(order_id_id=id,
                                                   invoice_number=invoice_number,
                                                   doctor_id=doctor_id,
                                                   store_id=store_id,
                                                   sgst=sgst,
                                                   cgst=cgst,
                                                   subtotal=subtotal,
                                                   old_credit=new_credit,
                                                   cash=cash,
                                                   online=online,
                                                   shipping=shipping_packing,
                                                   discount=discount,
                                                   pay_amount=total,
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
                hsn = float(medicine_data['hsn'])
                gst = float(medicine_data['gst'])
                taxable_amount = float(medicine_data['taxable_amount'])
                tax = float(medicine_data['tax'])
                amount = float(medicine_data['amount'])

                MedicineOrderBillDetail.objects.create(head_id=head_id,
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
        old_credit_sum = \
            MedicineOrderBillHead.objects.filter(doctor_id=user.doctor.id).exclude(id=id).aggregate(Sum('old_credit'))[
                'old_credit__sum'] or 0
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
            'invoice_number': user.invoice_number,
            'medicine': medicine_list,
            'old_credit_sum': old_credit_sum,
        }
        if order_type == 1:
            return render(request, 'order_tax_invoice_in_state.html', context)
        elif order_type == 2:
            return render(request, 'order_tax_invoice_other_state.html', context)
        elif order_type == 3:
            return render(request, 'oder_bill_of_supply.html', context)
        else:
            return render(request, 'oder_bill_of_supply.html', context)


@login_required(login_url='/account/user_login/')
def update_medicine_order_bill(request, order_type, id):
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
        new_credit = float(form.get('new_credit'))

        obj = MedicineOrderBillHead.objects.filter(id=id).update(store_id=store_id,
                                                                 sgst=sgst,
                                                                 cgst=cgst,
                                                                 subtotal=subtotal,
                                                                 old_credit=new_credit,
                                                                 cash=cash,
                                                                 online=online,
                                                                 shipping=shipping_packing,
                                                                 discount=discount,
                                                                 pay_amount=total,
                                                                 )
        if obj:
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
                hsn = float(medicine_data['hsn'])
                gst = float(medicine_data['gst'])
                taxable_amount = float(medicine_data['taxable_amount'])
                tax = float(medicine_data['tax'])
                amount = float(medicine_data['amount'])
                query = Q(head_id=head_id, medicine_id=medicine_id)
                already_obj = MedicineOrderBillDetail.objects.filter(query)
                if already_obj:
                    MedicineOrderBillDetail.objects.filter(query).update(record_qty=record_qty,
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
                        pre_sell_qty = already_obj[0].sell_qty
                        remaining_qty = int(record_qty + pre_sell_qty) - int(sell_qty)
                        MedicineStore.objects.filter(to_store_id=store_id, medicine_id=medicine_id).update(
                            qty=remaining_qty)
                else:
                    MedicineOrderBillDetail.objects.create(head_id=head_id,
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
                if sell_qty <= record_qty:
                    remaining_qty = int(record_qty) - int(sell_qty)
                    print(remaining_qty, '==========remaining_qty')
                    MedicineStore.objects.filter(to_store_id=store_id, medicine_id=medicine_id).update(
                        qty=remaining_qty)
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
        old_credit_sum = \
            MedicineOrderBillHead.objects.filter(doctor_id=user.doctor.id).exclude(id=id).aggregate(Sum('old_credit'))[
                'old_credit__sum'] or 0
        medicine = MedicineOrderBillDetail.objects.filter(head_id=id)
        medicine_list = []

        for i in medicine:
            data_dict = {}
            query = Q(to_store_id=store_id, medicine_id=i.medicine.id)
            store_medicine = MedicineStore.objects.filter(query).values('qty', 'price')
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
        }
        if order_type == 1:
            return render(request, 'update_medicine_order_bill_instate.html', context)
        elif order_type == 2:
            return render(request, 'order_tax_invoice_other_state.html', context)
        elif order_type == 3:
            return render(request, 'oder_bill_of_supply.html', context)
        else:
            return render(request, 'oder_bill_of_supply.html', context)


@login_required(login_url='/account/user_login/')
def estimate_medicine_order_bill(request, order_type, id):
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

        medicines = json.loads(request.POST.get('medicines'))
        doctor_id = form.get('doctor_id')
        oder_id = form.get('oder_id')
        invoice_number = form.get('invoice_number')
        subtotal = float(form.get('sub_total'))
        sgst = form.get('sgst')
        cgst = form.get('cgst')
        cash = float(form.get('cash'))
        online = float(form.get('online'))
        shipping_packing = int(form.get('shipping_packing'))
        discount = int(form.get('total_discount'))
        total = float(form.get('total'))
        new_credit = float(form.get('new_credit'))

        obj = EstimateMedicineOrderBillHead.objects.create(order_id_id=oder_id,
                                                           doctor_id=doctor_id,
                                                           store_id=store_id,
                                                           invoice_number=invoice_number,
                                                           sgst=sgst,
                                                           cgst=cgst,
                                                           subtotal=subtotal,
                                                           old_credit=new_credit,
                                                           cash=cash,
                                                           online=online,
                                                           shipping=shipping_packing,
                                                           discount=discount,
                                                           pay_amount=total,
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
                hsn = float(medicine_data['hsn'])
                gst = float(medicine_data['gst'])
                taxable_amount = float(medicine_data['taxable_amount'])
                tax = float(medicine_data['tax'])
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

        user = MedicineOrderBillHead.objects.get(id=id)
        oder_id = user.order_id.id
        invoice_number = user.invoice_number
        old_credit_sum = \
            MedicineOrderBillHead.objects.filter(doctor_id=user.doctor.id).exclude(id=id).aggregate(Sum('old_credit'))[
                'old_credit__sum'] or 0
        medicine = MedicineOrderBillDetail.objects.filter(head_id=id)
        medicine_list = []

        for i in medicine:
            data_dict = {}
            query = Q(to_store_id=store_id, medicine_id=i.medicine.id)
            store_medicine = MedicineStore.objects.filter(query).values('qty', 'price')
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
            return render(request, 'estimate_medicine_order_bill_instate.html', context)
        elif order_type == 2:
            return render(request, 'order_tax_invoice_other_state.html', context)
        elif order_type == 3:
            return render(request, 'oder_bill_of_supply.html', context)
        else:
            return render(request, 'oder_bill_of_supply.html', context)


@login_required(login_url='/account/user_login/')
def update_estimate_medicine_order_bill(request, order_type, id):
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
        msg = 'Estimated Bill updated failed.'
        medicines = json.loads(request.POST.get('medicines'))
        subtotal = float(form.get('sub_total'))
        sgst = form.get('sgst')
        cgst = form.get('cgst')
        cash = float(form.get('cash'))
        online = float(form.get('online'))
        shipping_packing = int(form.get('shipping_packing'))
        discount = int(form.get('total_discount'))
        total = float(form.get('total'))
        new_credit = float(form.get('new_credit'))
        obj = EstimateMedicineOrderBillHead.objects.filter(id=id).update(store_id=store_id,
                                                                         sgst=sgst,
                                                                         cgst=cgst,
                                                                         subtotal=subtotal,
                                                                         old_credit=new_credit,
                                                                         cash=cash,
                                                                         online=online,
                                                                         shipping=shipping_packing,
                                                                         discount=discount,
                                                                         pay_amount=total,
                                                                         )
        if obj:
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
                hsn = float(medicine_data['hsn'])
                gst = float(medicine_data['gst'])
                taxable_amount = float(medicine_data['taxable_amount'])
                tax = float(medicine_data['tax'])
                amount = float(medicine_data['amount'])
                query = Q(head_id=head_id, medicine_id=medicine_id)
                already_obj = EstimateMedicineOrderBillDetail.objects.filter(query)
                if already_obj:
                    EstimateMedicineOrderBillDetail.objects.filter(query).update(record_qty=record_qty,
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
            EstimateMedicineOrderBillHead.objects.filter(id=id).update(status=1)
            EstimateMedicineOrderBillDetail.objects.filter(head_id=id).exclude(medicine_id__in=medicine_ids).delete()
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

        user = EstimateMedicineOrderBillHead.objects.get(id=id)
        old_credit_sum = \
            EstimateMedicineOrderBillHead.objects.filter(doctor_id=user.doctor.id).exclude(id=id).aggregate(
                Sum('old_credit'))[
                'old_credit__sum'] or 0
        medicine = EstimateMedicineOrderBillDetail.objects.filter(head_id=id)
        medicine_list = []

        for i in medicine:
            data_dict = {}
            query = Q(to_store_id=store_id, medicine_id=i.medicine.id)
            store_medicine = MedicineStore.objects.filter(query).values('qty', 'price')
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
        }
        if order_type == 1:
            return render(request, 'update_estimate_medicine_order_bill_instate.html', context)
        elif order_type == 2:
            return render(request, 'order_tax_invoice_other_state.html', context)
        elif order_type == 3:
            return render(request, 'oder_bill_of_supply.html', context)
        else:
            return render(request, 'oder_bill_of_supply.html', context)


@login_required(login_url='/account/user_login/')
def view_normal(request, id):
    user_id = request.session['user_id']
    try:
        store = Store.objects.get(user_id=user_id)
        store_id = store.id
    except:
        store_id = 0
    print(id, '==============id=============')
    user = MedicineOrderBillHead.objects.get(order_id_id=id)
    order_type = user.order_type
    old_credit_sum = \
        MedicineOrderBillHead.objects.filter(doctor_id=user.doctor.id).exclude(id=id).aggregate(Sum('old_credit'))[
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
    print(medicine_list, '==================medicine_list')
    context = {
        'id': id,
        'order_type': order_type,
        'store_id': store_id,
        'user': user,
        'medicine': medicine_list,
        'old_credit_sum': old_credit_sum,
    }
    if order_type == 1:
        return render(request, 'view_normal_instate.html', context)
    elif order_type == 2:
        return render(request, 'order_tax_invoice_other_state.html', context)
    elif order_type == 3:
        return render(request, 'oder_bill_of_supply.html', context)
    else:
        return render(request, 'oder_bill_of_supply.html', context)


@login_required(login_url='/account/user_login/')
def view_estimate(request, id):
    user_id = request.session['user_id']
    try:
        store = Store.objects.get(user_id=user_id)
        store_id = store.id
    except:
        store_id = 0

    user = EstimateMedicineOrderBillHead.objects.get(order_id_id=id)
    order_type = user.order_type
    old_credit_sum = \
        EstimateMedicineOrderBillHead.objects.filter(doctor_id=user.doctor.id).exclude(id=id).aggregate(Sum('old_credit'))[
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
    }
    if order_type == 1:
        return render(request, 'view_estimate_instate.html', context)
    elif order_type == 2:
        return render(request, 'order_tax_invoice_other_state.html', context)
    elif order_type == 3:
        return render(request, 'oder_bill_of_supply.html', context)
    else:
        return render(request, 'oder_bill_of_supply.html', context)
