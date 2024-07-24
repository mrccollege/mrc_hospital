from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render

from medicine.models import Medicine

from store.models import MainStoreMedicine, MainStoreMedicineTransaction

from store.models import Store


# Create your views here.
def add_medicine(request):
    if request.method == 'POST':
        form = request.POST
        medicine_name = form.get('medicine_name')
        medicine_qty = form.get('medicine_qty')
        medicine_manufacturer = form.get('medicine_manufacturer')
        medicine_expiry = form.get('medicine_expiry')
        medicine_expiry = datetime.now().date()
        status = 'failed'
        msg = 'Medicine not added.'
        try:
            medicine_obj = Medicine.objects.create(medicine_name=medicine_name,
                                                   medicine_manufacturer=medicine_manufacturer,
                                                   medicine_expiry=medicine_expiry,
                                                   )
            if medicine_obj:
                medicine_id = medicine_obj.id
                store_obj = Store.objects.filter(type='MAIN')
                if store_obj:
                    store_id = store_obj[0].id
                    main_store_medicine_obj = MainStoreMedicine.objects.create(store_id=store_id,
                                                                               medicine_id=medicine_id,
                                                                               qty=medicine_qty,
                                                                               )
                    if main_store_medicine_obj:
                        MainStoreMedicineTransaction.objects.create(store_id=store_id,
                                                                    medicine_name=medicine_name,
                                                                    qty=medicine_qty,
                                                                    medicine_manufacturer=medicine_manufacturer,
                                                                    medicine_expiry=medicine_expiry,

                                                                    )
                        status = 'success'
                        msg = 'Medicine successfully Added'

        except Exception as e:
            status = status
            msg = str(e)

        context = {
            'status': status,
            'msg': msg,
        }
        return JsonResponse(context)
    return render(request, 'add_medicine.html')
