from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('customers/', views.customers, name='customers'),
    path('rooms/', views.rooms, name='rooms'),
    path('booking/', views.booking, name='booking'),
    path('customers/updatecustomer/<int:id>', views.updatecustomer, name='updatecustomer'),
    path('customers/updatecustomer/updatecustomerrecord/<int:id>', views.updatecustomerrecord, name='updatecustomerrecord'),
    path('customers/deletecustomer/<int:id>', views.deletecustomer, name='deletecustomer')
]