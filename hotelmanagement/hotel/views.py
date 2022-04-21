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
            customer = Customers.objects.get(firstname=firstname,
                                                lastname=lastname,
                                                phone=phone)
            if not customer:
                customer = Customers(firstname=firstname,lastname=lastname,phone=phone)
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


def addcustomer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            phone = request.POST['phone']
            customer = Customers(firstname=firstname,lastname=lastname,phone=phone)
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
            return render(request, "booking.html", {'form':form})
    else:
        return render(request,'booking.html')


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