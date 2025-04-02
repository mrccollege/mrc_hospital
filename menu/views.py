from django.http import JsonResponse
from django.shortcuts import render
import json

from django.views.decorators.csrf import csrf_exempt
from .models import MenuMaster, MenuUser, MenuCategory
from store.models import Store

from patient.models import Patient

from doctor.models import Doctor


# Create your views here.
def assign_menu(request):
    return render(request, 'assign_menu.html')


def get_user_data(request):
    if request.method == 'GET':
        form = request.GET
        user_type = int(form.get('user_type'))
        if user_type == 1:
            user_data = Store.objects.all()
            menus = MenuCategory.objects.filter(menu_purpose__title='Store_Dashboard')
        elif user_type == 2:
            user_data = Doctor.objects.all()
            menus = MenuCategory.objects.filter(menu_purpose__title='Doctor_Dashboard')
        elif user_type == 3:
            user_data = Patient.objects.all()
            menus = MenuCategory.objects.filter(menu_purpose__title='Patient_Dashboard')
        else:
            user_data = []
            menus = []

        user_data_list = []
        for i in user_data:
            data_dict = {}
            data_dict['user_id'] = i.user.id
            data_dict['username'] = i.user.username
            data_dict['user_mobile'] = i.user.mobile
            user_data_list.append(data_dict)

        menu_list = []
        for i in menus:
            data_dict = {}
            data_dict['cat_id'] = i.id
            data_dict['cat_title'] = i.cat_title
            data_dict['cat_desc'] = i.cat_desc
            menu_list.append(data_dict)

        context = {
            'user_data_list': user_data_list,
            'menu_list': menu_list,
        }
        return JsonResponse(context)


def get_menu_data(request):
    if request.method == 'GET':
        form = request.GET
        menu_type = int(form.get('menu_type'))
        user_id = int(form.get('user_id'))
        assign_menus = MenuUser.objects.filter(menu__menu_category_id=menu_type, user_id=user_id).values_list('menu', flat=True)
        menus = MenuMaster.objects.filter(menu_category_id=menu_type)
        menus_data_list = []
        for i in menus:
            data_dict = {}
            data_dict['menu_id'] = i.id
            data_dict['menu_title'] = i.menu_title
            data_dict['menu_url'] = i.menu_url
            if i.id in assign_menus:
                data_dict['is_selected'] = True
            else:
                data_dict['is_selected'] = False
            menus_data_list.append(data_dict)

        context = {
            'menus_data_list': menus_data_list,
        }
        return JsonResponse(context)


@csrf_exempt  # Only use if CSRF token is not handled in AJAX
def save_selected_menus(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            selectedMenuIds = data.get("selectedMenuIds", [])
            unselectedMenuIds = data.get("unselectedMenuIds", [])
            user_id = data.get("user_id")

            for menu_id in selectedMenuIds:
                already = MenuUser.objects.filter(menu_id=menu_id, user_id=user_id).exists()
                if already:
                    pass
                else:
                    MenuUser.objects.create(menu_id=menu_id,user_id=user_id,)

            for menu_id in unselectedMenuIds:
                already = MenuUser.objects.filter(menu_id=menu_id, user_id=user_id).exists()
                if already:
                    MenuUser.objects.filter(menu_id=menu_id, user_id=user_id).delete()
                else:
                    pass

            return JsonResponse({"success": True, "message": "Menus saved successfully!"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Invalid request method."})
