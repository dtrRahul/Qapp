from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.

class Time(models.Model):
    time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=40, default=None)
    no_customers = models.IntegerField(default=0)


class Shop(models.Model):
    shopname = models.CharField(max_length=25)
    address = models.CharField(max_length=50)
    mobile = models.IntegerField()


class Customers(models.Model):
    firstname = models.CharField(max_length=25)
    lastname = models.CharField(max_length=25)
    email = models.CharField(max_length=50)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    comments = models.CharField(max_length=100)
    logid = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.TimeField(null=True, blank=True)
    shopdetails = models.CharField(max_length=100, default=0)
    hairdresser = models.CharField(max_length=100, default=0)


class Barbers(models.Model):
    name = models.CharField(max_length=40)
    status = models.CharField(max_length=40, default=None)
    shopname = models.CharField(max_length=25,  default=None)
    time = models.TimeField(null=True, blank=True)


