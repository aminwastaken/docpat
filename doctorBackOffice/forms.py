from django import forms
from doctorBackOffice.models import Appointment,Service,Bill

class AppointmentCreationForm(forms.ModelForm):
  
    class Meta:
        model = Appointment
        fields = ["doctor", "patient", "date","services"]

class ServiceCreationForm(forms.ModelForm):
  
    class Meta:
        model = Service
        fields = ["name", "price"]