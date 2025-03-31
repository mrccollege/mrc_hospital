from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from menu.models import MenuUser, MenuCategory
from decimal import Decimal
from account.models import User

from doctor.models import Doctor

from store.models import Store

from my_order.models import MedicineOrderHead, MedicineOrderBillHead, EstimateMedicineOrderBillHead

from patient.models import PatientEstimateMedicineBillHead, PatientMedicineBillHead

import pandas as pd
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from medicine.models import Medicine


# Create your views here.
@login_required(login_url='/account/user_login/')
def dashboard(request):
    user_id = request.session.get('user_id')
    is_doctor = Doctor.objects.filter(user_id=user_id)
    if is_doctor:
        try:
            user = User.objects.get(id=user_id)
            doctor = Doctor.objects.get(user_id=user.id)
            doctor_id = doctor.id
        except:
            doctor_id = 0

        order_count = MedicineOrderHead.objects.filter(doctor_id=doctor_id).count()
        context = {
            'order_count': order_count,
        }
        return render(request, 'doctor_dashboard.html', context)
    is_store = Store.objects.filter(user_id=user_id)
    if is_store:
        store_type = is_store[0].type
        new_order = MedicineOrderHead.objects.filter(status=0).count()
        normal_bill_order = MedicineOrderBillHead.objects.filter().count()
        estimate_bill_order = EstimateMedicineOrderBillHead.objects.filter(status=1).count()

        patient_normal_bill = PatientMedicineBillHead.objects.filter(status=1).count()
        patient_estimate_bill = PatientEstimateMedicineBillHead.objects.filter(status=1).count()
        context = {
            'store_type': store_type,
            'store_id': is_store[0].id,
            'new_order': new_order,
            'normal_bill_order': normal_bill_order,
            'estimate_bill_order': estimate_bill_order,
            'patient_normal_bill': patient_normal_bill,
            'patient_estimate_bill': patient_estimate_bill,
        }
        return render(request, 'store_dashboard.html', context)
    else:
        return render(request, 'index.html')


def get_menus(request):
    user_id = request.session.get('user_id')
    if user_id is not None:
        menu_users = MenuUser.objects.filter(user_id=user_id).select_related('menu', 'menu__menu_category')
        category_menus = {}
        try:
            for menu_user in menu_users:
                category_name = menu_user.menu.menu_category.cat_title
                menu_title = menu_user.menu.menu_title
                menu_url = menu_user.menu.menu_url
                if category_name not in category_menus:
                    category_menus[category_name] = []
                category_menus[category_name].append({'title': menu_title, 'url': menu_url})

            category_menu_list = [{'category': cat, 'menus': menus} for cat, menus in category_menus.items()]
        except:
            category_menu_list = []

        try:
            user_obj = User.objects.get(id=user_id)
            profile_name = user_obj.username
        except:
            profile_name = ''

        context = {
            'category_menu_list': category_menu_list,
            'profile_name': profile_name,
        }
        return JsonResponse(context)
    else:
        return redirect('/account/user_login/')


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
        return  int(value)
    except:
        return  int(0)


def upload_medicine_excel(request):
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
