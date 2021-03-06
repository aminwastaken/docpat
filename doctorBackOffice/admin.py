from django.contrib import admin
from doctorBackOffice.models import Appointment, Service, DoctorInfo, Bill


class AppointmentAdmin(admin.ModelAdmin):
    model = Appointment
    list_display = ["id", "doctor", "patient", "date", "get_services"]


class ServiceAdmin(admin.ModelAdmin):
    model = Service
    list_display = ["id", "name", "price"]


class DoctorInfoAdmin(admin.ModelAdmin):
    model = DoctorInfo
    list_display = ["id", "doctor", "speciality",
                    "description", "get_services"]

class BillAdmin(admin.ModelAdmin):
    model = Bill
    list_display = ["appointment","get_services_objects"]


admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(DoctorInfo, DoctorInfoAdmin)
admin.site.register(Bill, BillAdmin)
