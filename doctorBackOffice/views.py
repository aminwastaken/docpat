from django.shortcuts import render
from django.http import HttpResponse
from doctorBackOffice.models import Appointment,Bill


def index(request):
    return HttpResponse("Hello, world. You're at the future doctor back office.")


def appointment(request, id):
    appointment = Appointment.objects.get(id=id)
    return render(request, 'doctorBackOffice/appointment.html', {'appointment': appointment})

def bill(request, id):
    bill = Bill.objects.get(id=id)
    return render(request, 'doctorBackOffice/bill.html', {'bill': bill})
