from django.utils import timezone
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


def appointmentAll(request):

    doctor = CustomUser.objects.get(id=request.user.pk)

    appointments = Appointment.objects.filter(patient=request.user)

    appointments_futur = appointments.filter(date__gte=timezone.now())
    appointments_past = appointments.filter(date__lte=timezone.now())

    result_data = {
        'appointments': appointments_past,
        'appointments_futur': appointments_futur
    }
    return render(request, 'doctorBackOffice/appointmentList.html', result_data)

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
    return HttpResponseRedirect('/dbo/doctor/' + str(doctorInfo.doctor.id))


def doctor(request, id):
    if request.method == 'POST':
        print(request.POST)
        doctorInfo = DoctorInfo.objects.get(
            doctor=CustomUser.objects.get(id=id))
        doctor = CustomUser.objects.get(id=doctorInfo.doctor.id)
        appointment = Appointment(doctor=doctor, patient=request.user,
                                  date=request.POST['apointmentDate'], time=request.POST['apointmentTime'])
        appointment.save()
        bill = Bill(appointment=appointment)
        bill.save()
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


def doctor_info(request):
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


def calendar(request):
    appointments = Appointment.objects.filter(doctor=request.user)
    # sort dates
    appointments = appointments.order_by('date')
    # format put times inside date object
    formattedDates = []
    formattedDates.append({
        'date': appointments[0].date, 'appointments': []})
    if(len(appointments) > 0):
        current_date = appointments[0].date
        for appointment in appointments:
            if(appointment.date != current_date):
                current_date = appointment.date
                formattedDates.append({
                    'date': current_date, 'appointments': []})
                formattedDates[-1]['appointments'].append(appointment)
            else:
                formattedDates[-1]['appointments'].append(appointment)
    print(formattedDates)
    return render(request, 'calendar.html', {'formattedDates': formattedDates})


def doctorList(request):
    doctors = CustomUser.objects.filter(user_type="doctor")
    return render(request, 'doctorList.html', {'doctors': doctors})


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
            return HttpResponseRedirect('/dbo/doctor/' + str(request.user.id))
    else:
        form = DocServiceCreationForm()
    return render(request, 'doctor_service.html', {'form': form, 'id': id})
