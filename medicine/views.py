from datetime import datetime

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
from .models import Medicine, MedicineCategory
from django.core.files.storage import FileSystemStorage
from store.models import Store, MedicineStore, MedicineStoreTransactionHistory
from django.db.models import Case, When


# Create your views here.
def add_category(request):
    if request.method == 'POST':
        form = request.POST
        name = form.get('name')
        cat_obj = MedicineCategory.objects.create(name=name.title())
        cat_dict = {
            'id': cat_obj.id,
            'name': cat_obj.name,
        }
        if cat_obj:
            cat_obj = cat_dict
            status = 'success'
            msg = 'category registered successfully.'
        else:
            cat_obj = {}
            status = 'failed'
            msg = 'category registered failed.'

        context = {
            'status': status,
            'msg': msg,
            'cat_obj': cat_obj,
        }
        return JsonResponse(context)

    else:
        return render(request, 'add_medicine_category.html')


def update_category(request, id):
    if request.method == 'POST':
        form = request.POST
        name = form.get('name')
        cat_obj = MedicineCategory.objects.filter(id=id).update(name=name.title())
        if cat_obj:
            status = 'success'
            msg = 'category updated successfully.'
        else:
            status = 'failed'
            msg = 'category updated failed.'

        context = {
            'status': status,
            'msg': msg,
        }
        return JsonResponse(context)
    else:
        category = MedicineCategory.objects.get(id=id)
        context = {
            'id': id,
            'category': category,
        }
        return render(request, 'update_medicine_category.html', context)


def all_medicine_category(request):
    category = MedicineCategory.objects.all()
    context = {
        'category': category,
    }
    return render(request, 'all_medicine_category.html', context)


def add_medicine(request):
    if request.method == 'POST':
        form = request.POST
        form1 = request.FILES
        name = form.get('name')
        price = float(form.get('price'))
        image = form1.get('image')
        category = form.get('category')
        video_link = form.get('video_link')
        manufacture = form.get('manufacture')
        mobile = form.get('mobile')
        recommend_medicine = form.get('recommend_medicine')
        status = 'failed'
        msg = 'Something went wrong.'
        try:
            medicine_obj = Medicine.objects.create(name=name.title(),
                                                   price=price,
                                                   category_id=category,
                                                   video_link=video_link,
                                                   manufacture=manufacture.title(),
                                                   mobile=mobile,
                                                   recom_to_doctor=recommend_medicine
                                                   )
            if medicine_obj:
                medicine_obj.image = image
                medicine_obj.save()
                status = 'success'
                msg = 'Medicine Added Successfully.'

        except Exception as e:
            status = status
            msg = str(e)

        context = {
            'status': status,
            'msg': msg,
        }
        return JsonResponse(context)
    else:
        category = MedicineCategory.objects.all()
        context = {
            'category': category
        }
        return render(request, 'add_medicine.html', context)


def medicine_update(request, id):
    if request.method == 'POST':
        form = request.POST
        form1 = request.FILES
        name = form.get('name')
        price = float(form.get('price'))
        image = form1.get('image')
        category = form.get('category')
        video_link = form.get('video_link')
        manufacture = form.get('manufacture')
        mobile = form.get('mobile')
        recommend_medicine = form.get('recommend_medicine')
        msg = 'Medicine Update Failed'
        status = 'Failed'
        try:
            medicine_obj = Medicine.objects.filter(id=id).update(name=name.title(),
                                                                 price=price,
                                                                 category=category,
                                                                 video_link=video_link,
                                                                 manufacture=manufacture.title(),
                                                                 mobile=mobile,
                                                                 recom_to_doctor=recommend_medicine
                                                                 )
            if medicine_obj:
                if image:
                    medicine_obj = Medicine.objects.filter(id=id)
                    medicine_obj.image = image
                    medicine_obj.save()
                msg = 'Medicine Update Successfully.'
                status = 'success'
        except Exception as e:
            msg = str(e)

        context = {
            'msg': msg,
            'status': status,
        }
        return JsonResponse(context)
    else:
        medicine = Medicine.objects.get(id=id)
        category = MedicineCategory.objects.annotate(category=Case(When(id=medicine.category.id, then=0),
                                                                   default=1))

        print(medicine.image, '================medicine=')
        context = {
            'id': id,
            'medicine': medicine,
            'category': category,
        }
        return render(request, 'update_medicine.html', context)


def add_medicine_to_store(request):
    if request.method == 'POST':
        form = request.POST
        store_id = int(form.get('store_id'))
        medicine_id = form.getlist('medicine_id')
        qty = form.getlist('qty')
        price = form.getlist('price')
        batch_no = form.getlist('batch_no')
        expiry_date = form.getlist('expiry_date')
        status = 'failed'
        try:
            for i in range(len(medicine_id)):
                query = Q(to_store_id=store_id, medicine_id=int(medicine_id[i]), batch_no=batch_no[i].upper())
                is_obj = MedicineStore.objects.filter(query)
                if is_obj:
                    pre_qty = is_obj[0].qty
                    total_qty = pre_qty + int(qty[i])
                    store_obj = MedicineStore.objects.filter(query).update(qty=total_qty)
                else:
                    store_obj = MedicineStore.objects.create(from_store_id=store_id,
                                                             to_store_id=store_id,
                                                             medicine_id=int(medicine_id[i]),
                                                             qty=int(qty[i]),
                                                             price=float(price[i]),
                                                             batch_no=batch_no[i].upper(),
                                                             expiry=datetime.strptime(expiry_date[i], "%d-%B-%Y"),
                                                             )

                if store_obj:
                    store_qty = MedicineStore.objects.get(query)
                    medicine = Medicine.objects.get(id=int(medicine_id[i]))
                    MedicineStoreTransactionHistory.objects.create(from_store_id=store_id,
                                                                   to_store_id=store_id,
                                                                   medicine_id=int(medicine_id[i]),
                                                                   medicine_name=medicine.name,
                                                                   category=medicine.category.name,
                                                                   price=float(price[i]),
                                                                   batch_no=batch_no[i].upper(),
                                                                   available_qty=store_qty.qty,
                                                                   add_qty=int(qty[i]),
                                                                   medicine_manufacture=medicine.manufacture,
                                                                   medicine_expiry=datetime.strptime(expiry_date[i], "%d-%B-%Y"),
                                                                   )

            status = 'success'
            msg = 'Medicine Added In Store Successfully.'

        except Exception as e:
            status = status
            msg = str(e)

        context = {
            'status': status,
            'msg': msg,
        }
        return JsonResponse(context)
    else:
        store = Store.objects.all()
        context = {
            'store': store
        }
        return render(request, 'add_medicine_to_store.html', context)


def view_record_medicine_detail(request, id):
    medicine_record = MedicineStore.objects.get(id=id)
    context = {
        'store_id': medicine_record.to_store.id,
        'medicine': medicine_record
    }
    return render(request, 'update_medicine_record.html', context)


def update_medicine_record(request):
    if request.method == 'POST':
        form = request.POST
        store_id = form.get('store_id')
        medicine_id = int(form.get('medicine_id'))
        medicine_name = form.get('medicine_name')
        category_name = form.get('category_name')
        category_id = form.get('category_id')
        batch_no = form.get('batch_no')
        price = form.get('price')
        medicine_qty = form.get('medicine_qty')
        add_medicine_qty = form.get('add_medicine_qty')
        minus_medicine_qty = form.get('minus_medicine_qty')
        manufacture = form.get('manufacture')
        mobile = form.get('mobile')
        medicine_expiry = form.get('medicine_expiry')
        medicine_expiry = datetime.strptime(medicine_expiry, "%d-%B-%Y")
        status = 'failed'
        msg = 'Medicine not added.'
        try:
            # Medicine.objects.filter(id=medicine_id).update(name=medicine_name,
            #                                                category_id=category_id,
            #                                                manufacture=manufacture,
            #                                                mobile=mobile,
            #                                                )
            store_obj = Store.objects.filter(id=store_id)
            if store_obj:
                to_store_id = store_obj[0].id
                query = Q(medicine_id=medicine_id, to_store_id=to_store_id, batch_no=batch_no)
                obj = MedicineStore.objects.get(query)
                total_qty = obj.qty
                if add_medicine_qty:
                    add_medicine_qty = add_medicine_qty
                    total_qty = obj.qty + int(add_medicine_qty)
                else:
                    add_medicine_qty = 0

                if minus_medicine_qty:
                    minus_medicine_qty = minus_medicine_qty
                    total_qty = obj.qty - int(minus_medicine_qty)
                else:
                    minus_medicine_qty = 0
                # main_store_medicine_obj = MedicineStore.objects.filter(query).update(qty=int(total_qty), expiry=medicine_expiry)
                main_store_medicine_obj = MedicineStore.objects.filter(query).update(qty=int(total_qty), price=price)
                if main_store_medicine_obj:
                    MedicineStoreTransactionHistory.objects.create(from_store_id=to_store_id,
                                                                   to_store_id=to_store_id,
                                                                   medicine_id=medicine_id,
                                                                   medicine_name=medicine_name,
                                                                   batch_no=obj.batch_no,
                                                                   category=category_name,
                                                                   price=obj.price,
                                                                   available_qty=total_qty,
                                                                   add_qty=add_medicine_qty,
                                                                   minus_qty=minus_medicine_qty,
                                                                   medicine_manufacture=obj.medicine.manufacture,
                                                                   medicine_expiry=medicine_expiry,
                                                                   )
                    status = 'success'
                    msg = 'Medicine Updated Successfully.'

        except Exception as e:
            status = status
            msg = str(e)

        context = {
            'status': status,
            'msg': msg,
        }
        return JsonResponse(context)


def all_medicine(request):
    medicine = Medicine.objects.all().order_by('-id')
    context = {
        'medicine': medicine,
    }
    return render(request, 'all_medicine.html', context)


def search_medicine(request):
    if request.method == 'GET':
        form = request.GET
        search_value = form.get('search_value')
        medicineIds = form.getlist('medicineIds[]')
        medicine = Medicine.objects.filter(name__icontains=search_value).exclude(id__in=medicineIds)
        data_list = []
        for i in medicine:
            data_dict = {}
            data_dict['id'] = i.id
            data_dict['name'] = i.name.capitalize()
            data_dict['category'] = str(i.category.name)
            data_list.append(data_dict)
        context = {
            'results': data_list,
        }
        return JsonResponse(context)


def upload_medicine_excel(request):
    if request.method == 'POST' and request.FILES.get('medicine_excel'):
        status = 'failed?'
        try:
            excel_file = request.FILES['medicine_excel']

            # Check if the file is an Excel file
            if not excel_file.name.endswith(('.xls', '.xlsx')):
                return JsonResponse({'msg': 'Invalid file format. Please upload an Excel file.'})

            # Save the file temporarily
            fs = FileSystemStorage()
            filename = fs.save(excel_file.name, excel_file)
            file_path = fs.path(filename)

            # Read the Excel file
            try:
                df = pd.read_excel(file_path)
            except Exception as e:
                fs.delete(filename)
                return JsonResponse({'msg': f'Error reading Excel file: {str(e)}'})

            # Normalize column names to avoid issues with case or extra spaces
            df.columns = df.columns.str.strip().str.lower()

            # Adjusted column mappings for normalized names
            column_mappings = {
                'medicine name': 'medicine_name',
                'medicine price': 'medicine_price',
                'medicine manufacturer/ supplier': 'medicine_manufacturer',
                'medicine type': 'type',
            }

            # Ensure that all required columns are present
            missing_columns = [col for col in column_mappings if col not in df.columns]
            if missing_columns:
                fs.delete(filename)
                return JsonResponse({'msg': f'Excel file is missing required columns: {", ".join(missing_columns)}'})

            # Proceed with data insertion
            for index, row in df.iterrows():
                medicine = Medicine(
                    medicine_name=row[column_mappings['medicine name']],
                    medicine_price=row[column_mappings['medicine price']],
                    type=row[column_mappings['medicine type']],
                    medicine_manufacturer=row[column_mappings['medicine manufacturer/ supplier']],
                )
                medicine.save()

            fs.delete(filename)
            status = 'success'
            msg = 'Excel sheet uploaded and processed successfully.'
        except Exception as e:
            print(e, '================e====================')
            msg = f"An error occurred: {str(e)}"
            status = status

        context = {
            'status': status,
            'msg': msg
        }
        return JsonResponse(context)

    return render(request, 'upload_medicine_excel.html')
