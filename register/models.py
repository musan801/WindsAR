from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class RegisterCustomer(models.Model):
    name = models.CharField(max_length=20)
    dob = models.DateField(max_length=10)
    winCoins = models.IntegerField(default=50)
    placesVisited = models.IntegerField(default=0)
    vouchers = models.IntegerField(default=0)
    user = models.OneToOneField(User,null = True,  on_delete=models.SET_NULL)

class BusinessOwner(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    category = models.CharField(max_length=20)
    latitude = models.FloatField(default=0000)
    longitude = models.FloatField(default=0000)
    user = models.OneToOneField(User,null = True, on_delete=models.SET_NULL)

class Voucher(models.Model):
    businessName = models.CharField(max_length=50)
    productName = models.CharField(max_length=50)
    discountPrice = models.IntegerField()
    expiryDate = models.DateField(max_length=10)
    actualPrice = models.IntegerField()
    winCoins = models.IntegerField()

class MarkerLocations(models.Model):
    locationName = models.CharField(max_length=50)
    locationLatitude = models.FloatField(default=0000)
    locationLongitude = models.FloatField(default=0000)
    description = models.CharField(max_length=500)
    imagelink= models.CharField(max_length=500)



