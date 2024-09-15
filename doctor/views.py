from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from doctor.models import Doctor

from account.models import User
from .models import PatientAppointmentHead, PatientMedicine, ChiefComplaints, PatientAppointmentDiagnosis, \
    OtherAssociatesComplaints
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
        form = request.POST
        user_id = request.session.get('user_id')
        doctor_id = Doctor.objects.get(user_id=user_id)
        doctor_id = doctor_id.id
        appointment_id = form.get('appointment_id')
        patient_id = form.get('patient_id')
        p_r = form.get('p_r')
        procto = form.get('procto')
        probing = form.get('probing')
        o_e = form.get('o_e')

        # ---------------------------------------------
        chief_complaints = form.get('chief_complaints')
        since = form.get('since')
        severity = form.get('severity')
        bleeding = form.get('bleeding')
        # ---------------------------------------------
        disease_name = form.get('disease_name')
        disease_position = form.get('disease_position')
        disease_type = form.get('disease_type')
        # ---------------------------------------------
        other_associates = form.getlist('other_associates')
        other_since = form.getlist('other_since')
        other_severity = form.getlist('other_severity')
        # ---------------------------------------------
        history = form.getlist('history')
        history_remark = form.getlist('history_remark')
        # ---------------------------------------------

        medicine_id = form.getlist('medicine_id')
        medicine_qty = form.getlist('medicine_qty')
        medicine_type = form.getlist('medicine_type')
        medicine_dose = form.getlist('medicine_dose')
        medicine_interval = form.getlist('medicine_interval')
        medicine_with = form.getlist('medicine_with')

        status = 'failed?'
        msg = 'Appointment Checked failed.'

        # ----------------------------------------------
        try:
            obj = PatientAppointmentHead.objects.create(doctor_id=doctor_id,
                                                        patient_id=patient_id,
                                                        p_r=p_r,
                                                        procto=procto,
                                                        probing=probing,
                                                        o_e=o_e,
                                                        )
            if obj:
                head_id = obj.id
                ChiefComplaints.objects.create(head_id=head_id,
                                               chief_complaints=chief_complaints,
                                               since_id=since,
                                               severity_id=severity,
                                               bleeding_id=bleeding,
                                               )

                PatientAppointmentDiagnosis.objects.create(head_id=head_id,
                                                           disease_id=disease_name,
                                                           position_id=disease_position,
                                                           type_id=disease_type,
                                                           )

                for i in range(len(other_associates)):
                    OtherAssociatesComplaints.objects.create(head_id=head_id,
                                                             complaints=other_associates[i],
                                                             since_id=other_since[i],
                                                             severity_id=other_severity[i],
                                                             )

                for i in range(len(medicine_id)):
                    PatientMedicine.objects.create(head_id_id=head_id,
                                                   medicine_id=int(medicine_id[i]),
                                                   qty=int(medicine_qty[i]),
                                                   medicine_type=medicine_type[i],
                                                   medicine_dose=medicine_dose[i],
                                                   medicine_interval=medicine_interval[i],
                                                   medicine_with=medicine_with[i],
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
