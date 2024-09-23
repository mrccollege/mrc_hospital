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
        doctor_id = form.get('doctor_id')
        subtotal = form.get('sub_total')
        discount = form.get('total_discount')
        shipping = form.get('shipping_packing')
        pay_amount = form.get('total')

        medicine_id = form.getlist('medicine_id')
        mrp = form.getlist('mrp')
        amount = form.getlist('amount')
        order_qty = form.getlist('order_qty')

        order_head = MedicineOrderHead.objects.create(doctor_id=doctor_id,
                                                      subtotal=subtotal,
                                                      discount=discount,
                                                      shipping=shipping,
                                                      pay_amount=pay_amount,
                                                      )

        if order_head:
            for i in range(len(medicine_id)):
                MedicineOrderDetail.objects.create(head_id=order_head.id,
                                                   medicine_id=medicine_id[i],
                                                   mrp=mrp[i],
                                                   order_qty=order_qty[i],
                                                   amount=amount[i],
                                                   )

            status = 'success'
            msg = 'order successfully created.'
        else:
            status = 'failed'
            msg = 'order failed.'

        context = {
            'status': status,
            'msg': msg,
        }

        return JsonResponse(context)

    else:
        user_id = request.session.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            doctor_id = Doctor.objects.get(user_id=user_id)
            doctor_id = doctor_id.id
        except:
            user = ''
            doctor_id = 0

        medicine = Medicine.objects.filter()
        context = {
            'medicine': medicine,
            'user': user,
            'doctor_id': doctor_id,
        }
        return render(request, 'medicine_order.html', context)
