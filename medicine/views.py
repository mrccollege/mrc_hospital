from datetime import datetime

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
from .models import Medicine, MedicineCategory
from django.core.files.storage import FileSystemStorage
from store.models import Store, MedicineStore, MedicineStoreTransactionHistory
from django.db.models import Case, When
from django.http import HttpResponse
from decimal import Decimal

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


def export_medicine_excel(request):
    # Fetch all medicine data
    medicines = Medicine.objects.all().values()

    # Convert queryset to a list of dictionaries
    medicine_list = list(medicines)

    # Convert timezone-aware DateTime fields to naive datetime
    for med in medicine_list:
        if med["created_at"]:
            med["created_at"] = med["created_at"].replace(tzinfo=None)
        if med["updated_at"]:
            med["updated_at"] = med["updated_at"].replace(tzinfo=None)

    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(medicine_list)

    # Rename columns for better readability (optional)
    df.rename(columns={
        "name": "Medicine Name",
        "price": "Price",
        "category_id": "Category ID",
        "desc": "Description",
        "video_link": "Video Link",
        "image": "Image Path",
        "manufacture": "Manufacture",
        "hsn": "HSN Code",
        "gst": "GST",
        "mobile": "Mobile",
        "recom_to_doctor": "Recommended to Doctor",
    }, inplace=True)

    # Create HTTP response with Excel content
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="registered_medicines.xlsx"'

    # Save DataFrame to Excel
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Medicines")

    return response


def clean_price(value):
    """Convert price from '100/-' to Decimal(100.00)"""
    if isinstance(value, str):
        value = value.replace('/-', '').strip()  # Remove '/-'
    try:
        return Decimal(value)  # Convert to Decimal
    except:
        return Decimal(0)  # Default value if conversion fails


def clean_gst(value):
    """Convert GST from '5%' to Decimal(0.05)"""
    if isinstance(value, str):
        value = value.replace('%', '').strip()  # Remove '%'
    try:
        return int(value)
    except:
        return int(0)


def register_medicine_excel(request):
    if request.method == "POST" and request.FILES.get("excel_file"):
        excel_file = request.FILES["excel_file"]
        fs = FileSystemStorage()
        file_path = fs.save(excel_file.name, excel_file)
        file_url = fs.url(file_path)

        # Read the Excel file
        df = pd.read_excel(fs.path(file_path))
        # Iterate and save data
        for _, row in df.iterrows():
            price = clean_price(row['MEDICINE PRICE'])
            gst = clean_price(row['GST'])
            Medicine.objects.create(
                name=row.get("MEDICINE NAME"),
                price=price,
                category_id=row.get("CATEGORY"),
                manufacture=row.get("MANUFACTURE"),
                mobile=row.get("MANUFACTURE_MOBILE"),
                desc=row.get("DESCRIPTION"),
                hsn=row.get("HSN"),
                gst=gst,
                recom_to_doctor=True,
            )

        return render(request, "upload_excel_medicine.html", {"success": "Data uploaded successfully!"})

    return render(request, "upload_excel_medicine.html")


def purchase_medicine_excel(request):
    if request.method == "POST" and request.FILES.get("excel_file"):
        user_id = request.session.get('user_id')
        store_data = Store.objects.filter(user_id=user_id)
        if store_data:
            store_id = store_data[0].id
        else:
            return render(request, "upload_excel_medicine.html")
        excel_file = request.FILES["excel_file"]
        fs = FileSystemStorage()
        file_path = fs.save(excel_file.name, excel_file)
        file_url = fs.url(file_path)

        # Read the Excel file
        df = pd.read_excel(fs.path(file_path))
        # Iterate and save data
        for _, row in df.iterrows():
            medicine_id = row.get('medicine_id')
            mini_record_qty = row.get('Min Required Qty')
            qty = row.get('Add Qty')
            batch_no = row.get('batch_no')
            expiry_date = row.get('Expiry Date')
            expiry_date_formatted = expiry_date.strftime("%Y-%m-%d")
            price = clean_price(row['MEDICINE PRICE'])
            is_obj = MedicineStore.objects.filter(to_store_id=store_id, medicine_id=int(medicine_id), batch_no=batch_no.upper())
            if is_obj:
                pre_qty = is_obj[0].qty
                total_qty = pre_qty + int(qty)
                MedicineStore.objects.filter(to_store_id=store_id, medicine_id=int(medicine_id), batch_no=batch_no.upper()).update(qty=total_qty, min_medicine_record_qty=int(mini_record_qty))
            else:
                MedicineStore.objects.create(from_store_id=store_id,
                                             to_store_id=store_id,
                                             medicine_id=medicine_id,
                                             min_medicine_record_qty=mini_record_qty,
                                             qty=qty,
                                             price=float(price),
                                             batch_no=batch_no.upper(),
                                             expiry=expiry_date_formatted,
                                             )

        return render(request, "upload_excel_medicine.html", {"success": "Data uploaded successfully!"})

    return render(request, "upload_excel_medicine.html")


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
        hsn = form.get('hsn')
        gst = form.get('gst')
        desc = form.get('desc')
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
                                                   hsn=hsn,
                                                   gst=gst,
                                                   desc=desc,
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
        hsn = form.get('hsn')
        gst = form.get('gst')
        desc = form.get('desc')
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
                                                                 hsn=hsn,
                                                                 gst=gst,
                                                                 desc=desc,
                                                                 recom_to_doctor=recommend_medicine
                                                                 )
            if medicine_obj:
                if image:
                    medicine_obj = Medicine.objects.get(id=id)
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
                                                                   default=1)).order_by('category')

        context = {
            'id': id,
            'medicine': medicine,
            'category': category,
        }
        return render(request, 'update_medicine.html', context)


def delete_medicine(request, id):
    try:
        deleted, _ = Medicine.objects.filter(id=id).delete()
        already_added = MedicineStore.objects.filter(medicine_id=id)
        if already_added:
            msg = 'Medicine not found.'
            success = False
            return JsonResponse({'success': success, 'msg': msg})
        else:
            if deleted:
                msg = 'Medicine has been deleted.'
                success = True
            else:
                msg = 'Medicine not found.'
                success = False
    except Exception as e:
        msg = f'Error occurred: {str(e)}'
        success = False

    # Return a JSON response
    return JsonResponse({'success': success, 'msg': msg})


def add_medicine_to_store(request):
    user_id = request.session.get('user_id')
    if request.method == 'POST':
        form = request.POST
        store_id = int(form.get('store_id'))
        medicine_id = form.getlist('medicine_id')
        mini_record_qty = form.getlist('mini_record_qty')
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
                    store_obj = MedicineStore.objects.filter(query).update(qty=total_qty, min_medicine_record_qty=int(
                        mini_record_qty[i]))
                else:
                    store_obj = MedicineStore.objects.create(from_store_id=store_id,
                                                             to_store_id=store_id,
                                                             medicine_id=int(medicine_id[i]),
                                                             min_medicine_record_qty=int(mini_record_qty[i]),
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
                                                                   medicine_expiry=datetime.strptime(expiry_date[i],
                                                                                                     "%d-%B-%Y"),
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
        store = Store.objects.filter(user_id=user_id)
        if store:
            store_type = store[0].type
            if store_type == 'MINI':
                store = Store.objects.filter(user_id=user_id)
            else:
                store = Store.objects.all()
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
        min_medicine_rec = form.get('min_medicine_rec')
        medicine_expiry = datetime.strptime(medicine_expiry, "%d-%B-%Y")
        status = 'failed'
        msg = 'Medicine not added.'
        # try:
        store_obj = Store.objects.filter(id=store_id)
        if store_obj:
            to_store_id = store_obj[0].id
            query = Q(medicine_id=medicine_id, to_store_id=to_store_id, batch_no=batch_no)
            obj = MedicineStore.objects.filter(query).update()
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

            main_store_medicine_obj = MedicineStore.objects.filter(query).update(qty=int(total_qty),
                                                                                 price=price,
                                                                                 batch_no=batch_no,
                                                                                 expiry=medicine_expiry,
                                                                                 min_medicine_record_qty=min_medicine_rec,
                                                                                 )
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

        # except Exception as e:
        #     status = status
        #     msg = str(e)

        context = {
            'status': status,
            'msg': msg,
        }
        return JsonResponse(context)


def all_medicine(request):
    medicine = Medicine.objects.all().order_by('-id')
    for i in medicine:
        print(i.name)
    context = {
        'medicine': medicine,
    }
    return render(request, 'all_medicine.html', context)


def search_medicine(request):
    if request.method == 'GET':
        form = request.GET
        search_value = form.get('search_value')
        medicineIds = form.getlist('medicineIds[]')
        medicine = Medicine.objects.filter(name__icontains=search_value)
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


def search_batch_no(request):
    if request.method == 'GET':
        form = request.GET
        search_value = form.get('search_value')
        batch_noIds = form.getlist('batch_noIds[]')
        print(batch_noIds, '=========batch_noIds=')
        store_id = int(form.get('store_id'))
        medicine = MedicineStore.objects.filter(batch_no__icontains=search_value, to_store=store_id).order_by(
            'medicine__name')
        data_list = []
        for i in medicine:
            data_dict = {}
            data_dict['id'] = i.id
            data_dict['batch_no'] = str(i.batch_no)
            data_dict['batch_lable'] = str(i.batch_no) + ' - ' + str(i.medicine.name)
            data_dict['medicine_id'] = str(i.medicine.id)
            data_dict['medicine_name'] = str(i.medicine.name)
            try:
                data_dict['min_medicine_record_qty'] = int(i.min_medicine_record_qty)
            except:
                data_dict['min_medicine_record_qty'] = 0
            data_dict['price'] = i.price
            data_list.append(data_dict)
        context = {
            'results': data_list,
        }
        return JsonResponse(context)
