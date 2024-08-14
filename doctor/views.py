from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from doctor.models import Doctor

from account.models import User

from .models import PatientAppointmentChecked, PatientAppointmentCheckedDetail
from appointment.models import PatientAppointment


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


@login_required(login_url='/account/user_login/')
def patient_appointment_checked(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        doctor_id = Doctor.objects.get(user_id=user_id)
        doctor_id = doctor_id.id
        form = request.POST
        appointment_id = form.get('appointment_id')
        patient_id = form.get('patient_id')
        doctor_diseases = form.get('doctor_diseases')
        patient_bp_min = form.get('patient_bp_min')
        patient_bp_max = form.get('patient_bp_max')
        medicine_id = form.getlist('medicine_id')
        medicine_qty = form.getlist('medicine_qty')
        status = 'failed?'
        msg = 'Appointment Checked failed.'

        try:
            obj = PatientAppointmentChecked.objects.create(doctor_id=doctor_id,
                                                           patient_id=patient_id,
                                                           doctor_diseases=doctor_diseases,
                                                           )
            if obj:
                head_id = obj.id
                for i in range(len(medicine_id)):
                    PatientAppointmentCheckedDetail.objects.create(head_id_id=head_id,
                                                                   medicine_id=int(medicine_id[i]),
                                                                   qty=int(medicine_qty[i]),
                                                                   )
                query = Q(id=appointment_id, patient_id=patient_id, doctor_id=doctor_id)
                PatientAppointment.objects.filter(query).update(appoint_status='checked')
                status = 'success'
                msg = 'Appointment Checked Successfully.'

        except Exception as e:
            msg = str(e)
            status = status

        context = {
            'msg': msg,
            'status': status,
        }
        return JsonResponse(context)
