from django.shortcuts import render


# Create your views here.
def medicine_order(request):
    return render(request, 'medicine_order.html')
