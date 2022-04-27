from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .models import Customers,Rooms
from datetime import datetime,timedelta
from .forms import CustomerForm

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


def booking(request):
    template = loader.get_template('booking.html')
    rooms = Rooms.objects.filter(customer_id__isnull=True).values().order_by('room_no')
    context = {
        'rooms': rooms,
        'min_in': datetime.today().strftime('%Y-%m-%d'),
        'max_in': (datetime.today() + timedelta(days=90)).strftime('%Y-%m-%d'),
    }
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            phone = request.POST['phone']
            customer,created = Customers.objects.get_or_create(firstname=firstname,
                                                lastname=lastname,
                                                phone=phone)
            customer.save()
            customer_id = customer.id
            room_no = request.POST['room']
            room = Rooms.objects.get(room_no=room_no)
            room.customer_id = customer_id
            room.check_in = request.POST['check_in']
            room.check_out = request.POST['check_out']
            room.save()
            return HttpResponseRedirect(reverse('customers'))
        else:
            context['form']=form
            return HttpResponse(template.render(context,request))
    else:
        form = CustomerForm()
        context['form']=form
        return HttpResponse(template.render(context,request))


def updatecustomer(request,id):
    template = loader.get_template('updatecustomer.html')
    customer = Customers.objects.get(id=id)
    rooms = Rooms.objects.filter(customer_id=id)
    context = {
        'customer':customer,
        'rooms':rooms,
        'min_in': datetime.today().strftime('%Y-%m-%d'),
        'max_in': (datetime.today() + timedelta(days=90)).strftime('%Y-%m-%d'),
    }
    return HttpResponse(template.render(context,request))


def updatecustomerrecord(request, id):
  first = request.POST['firstname']
  last = request.POST['lastname']
  phone = request.POST['phone']
  customer = Customers.objects.get(id=id)
  customer.firstname = first
  customer.lastname = last
  customer.phone = phone
  customer.save()
  return HttpResponseRedirect(reverse('customers'))


def deletecustomer(request, id):
    customer = Customers.objects.get(id=id)
    for room in Rooms.objects.filter(customer_id=id):
        room.customer_id = None
        room.check_in = None
        room.check_out = None
        room.save()
    customer.delete()
    return HttpResponseRedirect(reverse('customers'))


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