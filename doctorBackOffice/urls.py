from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('appointment/<int:id>', views.appointment, name='appointment'),
    path('bill/<int:id>', views.bill, name='bill'),
]