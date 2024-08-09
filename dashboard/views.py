from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from menu.models import MenuUser, MenuCategory


# Create your views here.
@login_required(login_url='/account/user_login/')
def dashboard(request):
    return render(request, 'index.html')


def get_menus(request):
    user_id = request.session.get('user_id')
    if user_id is not None:
        menu_users = MenuUser.objects.filter(user_id=user_id).select_related('menu', 'menu__menu_category')
        category_menus = {}

        for menu_user in menu_users:
            category_name = menu_user.menu.menu_category.cat_title
            menu_title = menu_user.menu.menu_title
            menu_url = menu_user.menu.menu_url
            if category_name not in category_menus:
                category_menus[category_name] = []
            category_menus[category_name].append({'title': menu_title, 'url': menu_url})

        category_menu_list = [{'category': cat, 'menus': menus} for cat, menus in category_menus.items()]
        return JsonResponse({'category_menu_list': category_menu_list})
    else:
        return redirect('/account/user_login/')


def data_table(request):
    return render(request, 'data.html')
