from django.shortcuts import render


# Create your views here.
def dashboard(request):
    return render(request, 'index.html')


def data_table(request):
    return render(request, 'data.html')
