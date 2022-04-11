# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from doctorBackOffice.models import Appointment,Service,DoctorInfo,Bill

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username", "user_type",
                    "address", "phone",]

class AppointmentAdmin(admin.ModelAdmin):
    model = Appointment
    list_display = ["id","doctor", "patient", "date","get_services"]

class ServiceAdmin(admin.ModelAdmin):
    model = Service
    list_display = ["name", "price"]

class DoctorInfoAdmin(admin.ModelAdmin):
    model = DoctorInfo
    list_display = ["doctor", "speciality", "description", "get_services"]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Service, ServiceAdmin)
