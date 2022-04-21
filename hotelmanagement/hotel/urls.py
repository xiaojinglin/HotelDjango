from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('customers/', views.customers, name='customers'),
    path('rooms/', views.rooms, name='rooms'),
    path('booking/', views.booking, name='booking'),
    path('booking/addcustomer/', views.addcustomer, name='addcustomer')
]