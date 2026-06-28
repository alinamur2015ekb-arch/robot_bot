from django.shortcuts import render 

from django.http import HttpResponse
from .models import Telemetry

def update_telemetry(request):
    temperatura = request.GET.get('temperatura')
    humidity = request.GET.get('humidity')
    status = request.GET.get('status')

    if temperatura and humidity and status:
        Telemetry.objects.create(
            temp=float(temperatura),
            humidity=float(humidity),
            status=status
        )
        return HttpResponse("Data saved successfully!", status=200)
    
    return HttpResponse("Missing parameters", status=400)
