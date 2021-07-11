from django.shortcuts import render,loader,redirect
from django.conf import settings
from django.http import HttpResponse

# Create your views here.

def mainindex(request):
    return render(request,'maintenence.html')

