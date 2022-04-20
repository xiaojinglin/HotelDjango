from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Customers,Rooms
from datetime import datetime,timedelta

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


def booking(request):
    rooms = Rooms.objects.filter(customer_id__isnull=True).values().order_by('room_no')
    template = loader.get_template('booking.html')
    context = {
        'rooms': rooms,
        'min_in': datetime.today().strftime('%Y-%m-%d'),
        'max_in': (datetime.today() + timedelta(days=90)).strftime('%Y-%m-%d')
    }
    return HttpResponse(template.render(context,request))


def customers(request):
    customers = Customers.objects.all().values()
    for c in customers:
        rooms = Rooms.objects.filter(customer_id=c['id']).values()
        c['rooms']=rooms
    template = loader.get_template('customers.html')
    context = {
        'customers': customers,
    }
    return HttpResponse(template.render(context,request))


def rooms(request):
    rooms = Rooms.objects.all().values().order_by('room_no')
    template = loader.get_template('rooms.html')
    context = {
        'rooms': rooms,
    }
    return HttpResponse(template.render(context,request))