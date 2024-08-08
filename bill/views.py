from django.shortcuts import render


# Create your views here.
def bill_list(request):
    return render(request, 'bill_list.html')
