from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from accounts.models import CustomUser
from doctorBackOffice.forms import DocPageCreationForm, DocServiceCreationForm
from doctorBackOffice.models import Appointment, Bill, DoctorInfo, Service
from accounts.forms import CustomUserChangeForm, CustomUserCreationForm
from django.http import HttpResponseRedirect


def index(request):
    return HttpResponse("Hello, world. You're at the future doctor back office.")


def appointment(request, id):
    appointment = Appointment.objects.get(id=id)
    return render(request, 'doctorBackOffice/appointment.html', {'appointment': appointment})


def bill(request, id):
    bill = Bill.objects.get(id=id)
    total = 0
    for service in bill.appointment.services.all():
        total += service.price
    return render(request, 'doctorBackOffice/bill.html', {'bill': bill, 'total': total})


def cancel_appointment(request, id):
    appointment = Appointment.objects.get(id=id)
    doctorInfo = DoctorInfo.objects.get(doctor=appointment.doctor)
    appointment.delete()
    return HttpResponseRedirect('/dbo/doctor/' + str(doctorInfo.id))


def doctor(request, id):
    if request.method == 'POST':
        print(request.POST)
        doctorInfo = DoctorInfo.objects.get(id=id)
        doctor = CustomUser.objects.get(id=doctorInfo.doctor.id)
        appointment = Appointment(doctor=doctor, patient=request.user,
                                  date=request.POST['apointmentDate'], time=request.POST['apointmentTime'])
        appointment.save()
        for service in request.POST.getlist('services'):
            appointment.services.add(Service.objects.get(id=service))
        appointment.save()
    doctor = CustomUser.objects.get(id=id)
    doctor_infos = DoctorInfo.objects.get(doctor=doctor)
    hours = [
        {"value": 9, "text": "09:00"},
        {"value": 10, "text": "10:00"},
        {"value": 11, "text": "11:00"},
        {"value": 12, "text": "12:00"},
        {"value": 13, "text": "13:00"},
        {"value": 14, "text": "14:00"},
        {"value": 15, "text": "15:00"},
        {"value": 16, "text": "16:00"},
        {"value": 17, "text": "17:00"},
        {"value": 18, "text": "18:00"},
        # check if appointment exists
    ]
    appointment_exist = Appointment.objects.filter(
        doctor=doctor, patient=request.user).exists()
    print("appointment_exist")
    print(appointment_exist)
    if appointment_exist:
        appointment = Appointment.objects.filter(
            doctor=doctor, patient=request.user).first()
        print(appointment.doctor)
    else:
        appointment = None
    return render(request, 'doctorBackOffice/doctor.html', {'doctor': doctor, 'doctor_infos': doctor_infos, 'hours': hours, 'appointment_exist': appointment_exist, 'appointment': appointment})


def profile(request):
    if request.method == 'POST':
        if (CustomUser.objects.get(id=request.user.id)).user_type == "doctor":
            instance = get_object_or_404(DoctorInfo, doctor=request.user)
            form = DocPageCreationForm(instance=instance)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/')
        else:
            print("USER PATIENT POST")
            form = CustomUserChangeForm()
            if form.is_valid():
                print("user save")
                form.save()
                # data = form.cleaned_data
                # currentUser = CustomUser.objects.get(id=request.user.id)
                # currentUser.first_name = data["First Name"]
                # currentUser.save()
                return HttpResponseRedirect('/')
    else:
        if (CustomUser.objects.get(id=request.user.id)).user_type == "doctor":
            doctor_info_id = DoctorInfo.objects.get(doctor=request.user).id
            instance = get_object_or_404(DoctorInfo, id=doctor_info_id)
            form = DocPageCreationForm(instance=instance) #update form
        else:
            print((CustomUser.objects.get(id=request.user.id).user_type))
            instance = get_object_or_404(CustomUser, id=request.user.id)
            form = CustomUserChangeForm(instance=instance)
    return render(request, 'profile.html', {'form': form, 'id': id})


def doctor_services(request):
    if request.method == 'POST':
        form = DocServiceCreationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            service = Service(name=data['name'], price=data['price'])
            service.save()
            doctor = DoctorInfo.objects.get(doctor=request.user)
            doctor.services.add(service)
            doctor.save()
            form.save()
            return HttpResponseRedirect('/dbo/doctor/' + str(doctor.id))
    else:
        form = DocServiceCreationForm()
    return render(request, 'doctor_service.html', {'form': form, 'id': id})
