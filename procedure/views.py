from .models import Procedure, ProcedureBillHead, ProcedureBillDetail
from my_order.views import normal_generate_invoice_number
import json
from datetime import datetime
from django.db.models import Q, Case, When
from django.http import JsonResponse
from patient.models import Patient, OtherReference, SocialMediaReference
from store.models import Store, MedicineStoreTransactionHistory
from django.shortcuts import render, redirect
from django.db.models.functions import Coalesce
from django.db.models import DecimalField
from django.db.models import Sum, F, FloatField, ExpressionWrapper








# Create your views here.
def patient_procedure(request):
    return render(request, 'patient_procedure_data.html')


def create_procedure(request, patient_id):
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

        subtotal = float(form.get('sub_total'))
        flat_discount = float(form.get('flat_discount'))
        discount = int(form.get('total_discount'))

        discount_amount = subtotal * discount / 100
        after_dis_amount = subtotal - discount_amount
        after_dis_amount = after_dis_amount - flat_discount

        cash = float(form.get('cash'))
        online = float(form.get('online'))

        obj = ProcedureBillHead.objects.create(invoice_number=invoice_number,
                                               patient_id=patient_id,
                                               store_id=store_id,
                                               subtotal=subtotal,
                                               flat_discount=flat_discount,
                                               discount_amount=discount_amount,
                                               cash=cash,
                                               online=online,
                                               discount=discount,
                                               pay_amount=after_dis_amount,
                                               status=1,
                                               )
        if obj:
            head_id = obj.id
            for medicine_data in medicines:
                medicine_id = medicine_data['medicine_id']
                code = medicine_data['code']
                sell_qty = int(medicine_data['sell_qty'])
                mrp = float(medicine_data['mrp'])
                amount = float(medicine_data['amount'])
                from_date = medicine_data['from_date']
                from_date = datetime.strptime(from_date, "%d-%m-%Y").date()
                to_date = medicine_data['to_date']
                to_date = datetime.strptime(to_date, "%d-%m-%Y").date()

                ProcedureBillDetail.objects.create(head_id=head_id,
                                                   procedure_id=medicine_id,
                                                   sell_qty=sell_qty,
                                                   rate=mrp,
                                                   amount=amount,
                                                   code=code,
                                                   from_date=from_date,
                                                   to_date=to_date,
                                                   )

            status = 'success'
            msg = 'Bill creation Successfully.'

        context = {
            'status': status,
            'msg': msg,
        }
        return JsonResponse(context)
    else:
        patient = Patient.objects.get(id=patient_id)
        context = {
            'patient_id': patient_id,
            'patient': patient,
        }
        return render(request, 'create_procedure.html', context)


def update_procedure(request, id):
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
        flat_discount = float(form.get('flat_discount'))
        discount1 = int(form.get('total_discount'))

        discount_amount = subtotal * discount1 / 100
        after_dis_amount = subtotal - discount_amount
        after_dis_amount = after_dis_amount - flat_discount

        cash = float(form.get('cash'))
        online = float(form.get('online'))

        head_id = id

        medicine_ids = []
        for medicine_data in medicines:
            medicine_id = medicine_data['medicine_id']
            medicine_ids.append(medicine_id)
            code = medicine_data['code']
            sell_qty = int(medicine_data['sell_qty'])
            mrp = float(medicine_data['mrp'])
            amount = float(medicine_data['amount'])
            from_date = medicine_data['from_date']
            from_date = datetime.strptime(from_date, "%d-%m-%Y").date()
            to_date = medicine_data['to_date']
            to_date = datetime.strptime(to_date, "%d-%m-%Y").date()
            already_obj = ProcedureBillDetail.objects.filter(head_id=head_id, procedure_id=medicine_id)

            if already_obj:
                ProcedureBillDetail.objects.filter(head_id=head_id, procedure_id=medicine_id).update(sell_qty=sell_qty,
                                                                                                     rate=mrp,
                                                                                                     amount=amount,
                                                                                                     code=code,
                                                                                                     from_date=from_date,
                                                                                                     to_date=to_date,
                                                                                                     )
            else:
                ProcedureBillDetail.objects.create(head_id=head_id,
                                                   procedure_id=medicine_id,
                                                   sell_qty=sell_qty,
                                                   rate=mrp,
                                                   amount=amount,
                                                   code=code,
                                                   from_date=from_date,
                                                   to_date=to_date,
                                                   )

        obj = ProcedureBillHead.objects.filter(id=id).update(store_id=store_id,
                                                             subtotal=subtotal,
                                                             flat_discount=flat_discount,
                                                             discount_amount=discount_amount,
                                                             cash=cash,
                                                             online=online,
                                                             discount=discount1,
                                                             pay_amount=after_dis_amount,
                                                             status=1,
                                                             )
        if obj:
            ProcedureBillDetail.objects.filter(head_id=id).exclude(procedure_id__in=medicine_ids).delete()
            status = 'success'
            msg = 'Bill creation Successfully.'

        context = {
            'status': status,
            'msg': msg,
        }
        return JsonResponse(context)

    else:
        user = ProcedureBillHead.objects.get(id=id)
        procedure = ProcedureBillDetail.objects.filter(head_id=id)
        context = {
            'id': id,
            'user': user,
            'procedure': procedure,
        }
        return render(request, 'update_procedure.html', context)


def view_procedure_invoice(request, id):
    user_id = request.session['user_id']
    try:
        store = Store.objects.get(user_id=user_id)
        store_id = store.id
    except:
        store_id = 0
    try:
        user = ProcedureBillHead.objects.get(id=id)
    except:
        return redirect('/procedure/ProcedureBillHead_list/')

    invoice_number = user.invoice_number
    cash_online_amount = ProcedureBillHead.objects.filter(patient_id=user.patient.user.id).exclude(id=id).aggregate(
        total=Sum(
            Coalesce(F('cash'), 0) +
            Coalesce(F('online'), 0) +
            Coalesce(F('extra_cash_amount'), 0) +
            Coalesce(F('extra_online_amount'), 0),
            output_field=DecimalField()
        )
    )['total'] or 0

    total_pay_amount = ProcedureBillHead.objects.filter(patient_id=user.patient.user.id).exclude(id=id).aggregate(
        total=Sum('pay_amount')
    )['total'] or 0

    old_credit_sum = total_pay_amount - cash_online_amount

    pay_amount = user.pay_amount
    cash = user.cash
    online = user.online

    remaining_amount = pay_amount - (cash + online) + old_credit_sum

    medicine = ProcedureBillDetail.objects.filter(head_id=user.id)

    grand_sub_total = 0

    subtotal_amount = medicine.aggregate(total_amount=Sum(F('sell_qty') * F('rate')))['total_amount'] or 0

    context = {
        'id': id,
        'store_id': store_id,
        'user': user,
        'medicine': medicine,
        'subtotal_amount': subtotal_amount,
        'grand_sub_total': grand_sub_total,

        'remaining_amount': remaining_amount,
        'old_credit_sum': old_credit_sum,
        'invoice_number': invoice_number,
    }

    return render(request, 'procedure_invoice.html', context)


def procedure_list(request):
    procedure = ProcedureBillHead.objects.all().order_by('-id')
    context = {
        'procedure': procedure,
    }
    return render(request, 'procedure_list.html', context)


def get_procedure(request):
    if request.method == 'GET':
        form = request.GET
        search_value = form.get('search_value', '').strip()
        procedure_ids = form.getlist('procedure_ids[]')
        query = ~Q(id__in=procedure_ids)
        if search_value:
            search_terms = search_value.split()
            for term in search_terms:
                query &= Q(name__icontains=term)

        medicines = Procedure.objects.filter(query).values('id', 'name', 'price')
        data_list = [
            {
                'id': i['id'],
                'name': i['name'].capitalize(),
                'mrp': i['price'],
            }
            for i in medicines
        ]
        context = {'results': data_list}
        return JsonResponse(context)
