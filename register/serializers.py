from django.db.models import fields
from rest_framework import serializers
from .models import RegisterCustomer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterCustomer
        fields = ['id']
