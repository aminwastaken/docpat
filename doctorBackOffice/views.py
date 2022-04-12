from django.shortcuts import render
from django.http import HttpResponse
from accounts.models import CustomUser
from doctorBackOffice.forms import DocPageCreationForm, DocServiceCreationForm
from doctorBackOffice.models import Appointment, Bill, DoctorInfo, Service
from django.http import HttpResponseRedirect


def index(request):
    return HttpResponse("Hello, world. You're at the future doctor back office.")


def appointment(request, id):
    appointment = Appointment.objects.get(id=id)
    return render(request, 'doctorBackOffice/appointment.html', {'appointment': appointment})


def bill(request, id):
    bill = Bill.objects.get(id=id)
    return render(request, 'doctorBackOffice/bill.html', {'bill': bill})


def doctor(request, id):
    doctor = CustomUser.objects.get(id=id)
    doctor_infos = DoctorInfo.objects.get(doctor=doctor)
    return render(request, 'doctorBackOffice/doctor.html', {'doctor': doctor, 'doctor_infos': doctor_infos})


def doctor_info(request, id):
    if request.method == 'POST':
        form = DocPageCreationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            currentUser = CustomUser.objects.get(id=request.user.id)
            doctor = DoctorInfo(
                doctor=request.user, speciality=data['speciality'], description=data['description'])
            doctor.save()
            return HttpResponseRedirect('/')
    else:
        form = DocPageCreationForm()
    return render(request, 'doctor_info.html', {'form': form, 'id': id})


def doctor_services(request, id):
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
            return HttpResponseRedirect('/')
    else:
        form = DocServiceCreationForm()
    return render(request, 'doctor_service.html', {'form': form, 'id': id})
