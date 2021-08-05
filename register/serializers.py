from django.db.models import fields
from rest_framework import serializers
from .models import RegisterCustomer
from django.contrib.auth.models import User

from register import models

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterCustomer
        fields = '__all__'

class fetchAuthDetails(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ['id','email','username']

class updateCoins(serializers.ModelSerializer):
    class Meta:
        model= RegisterCustomer
        fields = ['id','winCoins']

