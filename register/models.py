from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class RegisterCustomer(models.Model):
    name = models.CharField(max_length=20)
    dob = models.DateField(max_length=10)
    user = models.OneToOneField(User,null = True,  on_delete=models.SET_NULL)

