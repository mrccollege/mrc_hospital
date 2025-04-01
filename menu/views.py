from django.http import JsonResponse
from django.shortcuts import render

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
        menus = MenuMaster.objects.filter(menu_category_id=menu_type)

        menus_data_list = []
        for i in menus:
            data_dict = {}
            data_dict['user_id'] = i.user.id
            data_dict['username'] = i.user.username
            data_dict['user_mobile'] = i.user.mobile
            menus_data_list.append(data_dict)

        context = {
            'menus_data_list': menus_data_list,
        }
        return JsonResponse(context)
