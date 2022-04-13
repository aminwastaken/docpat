from django import forms
from doctorBackOffice.models import Appointment, DoctorInfo, Service, Bill


class AppointmentCreationForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ["doctor", "patient", "date", "services"]


class ServiceCreationForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = ["name", "price"]


class DocPageCreationForm(forms.ModelForm):
    class Meta:
        model = DoctorInfo
        fields = ["speciality", "description"]


class DocServiceCreationForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["name", "price"]