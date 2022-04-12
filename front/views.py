from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def doctorlist(request):
    return HttpResponse('List of doctors')
