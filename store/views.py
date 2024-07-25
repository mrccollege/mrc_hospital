from django.shortcuts import render

from .models import MainStoreMedicine, Store


# Create your views here.
def main_store(request):
    store = MainStoreMedicine.objects.all()
    store_name = store[0].store
    context = {
        'store_name': store_name,
        'store': store
    }
    return render(request, 'main_store_detail.html', context)


def mini_store(request):
    store = Store.objects.filter(type='MINI').order_by('-id')
    print(store)
    context = {
        'store': store
    }
    return render(request, 'mini_store_detail.html', context)
