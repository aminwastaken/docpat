from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('appointment/<int:id>', views.appointment, name='appointment'),
    path('bill/<int:id>', views.bill, name='bill'),
    path('profile', views.profile, name='profile'),
    path('doctor/<int:id>', views.doctor, name='doctor'),
    path('doctor/services', views.doctor_services, name='doctor_services'),
    path('appointment/cancel/<int:id>',
         views.cancel_appointment, name='cancel_appointment'),
]
