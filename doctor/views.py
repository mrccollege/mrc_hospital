from django.shortcuts import render


# Create your views here.
def list_doctor(request):
    return render(request, 'doctor_list.html')
