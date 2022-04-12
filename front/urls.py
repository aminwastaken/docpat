from django.views.generic.base import TemplateView
from django.urls import path, include
from django.contrib import admin
from . import views


urlpatterns = [
    path('', views.doctorlist, name='doctorlist'),
]
