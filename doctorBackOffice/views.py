from django.shortcuts import render
from django.http import HttpResponse
from accounts.models import CustomUser
from doctorBackOffice.models import Appointment,Bill, DoctorInfo


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
