from ast import mod
from django.db import models

class Customers(models.Model):
    id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)


class Rooms(models.Model):
    id = models.AutoField(primary_key=True)
    room_no = models.CharField(max_length=50)
    customer_id = models.IntegerField(null=True)
    room_type = models.CharField(max_length=50)
    price = models.IntegerField(null=True)
    check_in = models.DateField(null=True)
    check_out = models.DateField(null=True)