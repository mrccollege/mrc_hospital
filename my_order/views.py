import json

from django.http import JsonResponse
from django.shortcuts import render

from medicine.models import Medicine

from account.models import User

from store.models import MedicineStore

from my_order.models import MedicineOrderDetail

from doctor.models import Doctor

from my_order.models import MedicineOrderHead


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
        shipping = form.get('shipping_packing')
        pay_amount = form.get('total')

        print(doctor_id, '===========doctor_id')
        print(shipping, '===========shipping')
        # try:
        order_head = MedicineOrderHead.objects.create(doctor_id=doctor_id,
                                                      subtotal=subtotal,
                                                      discount=discount,
                                                      shipping=shipping,
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

        # except Exception as e:
        #     status = 'failed'
        #     msg = str(e)

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
