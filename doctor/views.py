from django.http import JsonResponse
from django.shortcuts import render

from doctor.models import Doctor

from account.models import User


# Create your views here.
def doctor_list(request):
    doctor = Doctor.objects.all()
    context = {
        'doctor': doctor
    }
    return render(request, 'doctor_list.html', context)


def doctor_detail(request, id):
    if request.method == 'POST':
        form = request.POST
        username = form.get('doctor_name')
        mobile = form.get('mobile')
        email = mobile + 'yopmail.com'
        password = form.get('password')
        phone = form.get('phone')
        address = form.get('address')
        specialist = form.get('specialist')
        degree = form.get('degree')
        status = 'failed'
        msg = 'Doctor Detail updated failed.'
        try:
            user_obj = Doctor.objects.filter(id=id).update(specialist=specialist.upper(),
                                                           degree=degree.upper()
                                                           )
            if user_obj:
                user_id = Doctor.objects.get(id=id)
                user_id = user_id.user.id
                User.objects.filter(id=user_id).update(username=username,
                                                       email=email,
                                                       mobile=mobile,
                                                       phone=phone,
                                                       address=address)
            if password:
                u = User.objects.get(id=user_id)
                u.set_password(password)
                u.save()

            if user_obj:
                status = 'success'
                msg = 'Doctor Detail updated successfully.'

        except Exception as e:
            status = status
            msg = str(e)

        context = {
            'status': status,
            'msg': msg,
        }
        return JsonResponse(context)
    else:
        doctor = Doctor.objects.get(id=id)
        context = {
            'id': id,
            'doctor': doctor
        }
        return render(request, 'doctor_detail.html', context)
