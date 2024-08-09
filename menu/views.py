from django.http import JsonResponse
from django.shortcuts import render

from .models import MenuMaster, MenuUser
from store.models import Store


# Create your views here.
def assigne_menu(request):
    if request.method == 'POST':
        form = request.POST
        user_id = form.get('user_id')
        checked_values = form.getlist('checked_values[]')
        status = 'failed'
        try:
            MenuUser.objects.filter(user_id=user_id).delete()
            for i in range(len(checked_values)):
                MenuUser.objects.create(user_id=user_id,
                                        menu_id=checked_values[i]
                                        )
            status = 'success'
            msg = 'Menu assigned successfully.'
        except Exception as e:
            msg = str(e)

        context = {
            'status': status,
            'msg': msg,
        }
        return JsonResponse(context)
    else:
        store_user = Store.objects.filter()
        menu = MenuMaster.objects.all()
        context = {
            'store_user': store_user,
            'menu': menu
        }
        return render(request, 'assigne_menu.html', context)
