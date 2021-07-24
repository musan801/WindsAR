from django.contrib.auth import models
from django.http import response
from django.shortcuts import render
from django.db import transaction

from django.contrib.auth.models import User
# Create your views here.
from .models import RegisterCustomer
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth import authenticate
import traceback
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny, NOT
from .models import BusinessOwner
from .serializers import CustomerSerializer
from rest_framework import status
from rest_framework import viewsets
from . import serializers

class RegisterCustomerView(generics.GenericAPIView):
    @transaction.atomic
    def post(self,request):
        try:
            email = username = request.data.get("email").strip()
            password = request.data.get("password")
            name = request.data.get("name")
            dob = request.data.get('dob')       
            # dob format yyyy/mm/dd

            user = User.objects.filter(email=email).last()
            if user != None:
                return Response({"error" : 'Email already exists. Please enter another ID'.format(request.data.get("email"))},status=400)
            else:
                user = User.objects.create_user(
                    username, email, password,
                )

                customer = RegisterCustomer()
                customer.user_id = user.id
                customer.name = name
                customer.dob = dob
                customer.save()

                response = {
                            'success': 'True',
                            'message': 'User logged in successfully',
                            'user_email': user.email,
                            'customer_name': customer.name,
                            'customer_dob' : customer.dob,
                            'user_id': user.id,
                            'customer_id': customer.id,
                        }

                return Response(response,status=201)
        except Exception as e:
            print(traceback.format_exc())
            return Response({'errorNeel': '{}'.format(e)},status=400)


class LoginCustomer(generics.GenericAPIView):
    def post(self,request):
        try:
            username = request.data.get("email",None)
            password = request.data.get("password",None)
            # id = request.data.get("id",None)
            
            loginCheck = authenticate(username=username, password=password)
           
            if loginCheck is None:
                customer_email = User.objects.filter(username=username).first()
                if customer_email is None:
                    return Response({"error":'User with this email and password is not found'})
                else:
                    return Response({"error":'Incorrect Password'})
            else:
                # entireData = User.objects.filter(username=username)
                # getData = CustomerSerializer(entireData,many=True)
                # cusID = getData.data
                # print(cusID)
                
                # allDetails = RegisterCustomer.objects.filter(id=)

                response= {
                        'success': 'True',
                        'message':'User logged In successfully',
                    }
                
                return Response(response,status=201)
        except Exception as e:
            print(traceback.format_exc())
            return Response({'error': '{}'.format(e)},status=400)


class RegisterBusinessView(generics.GenericAPIView):
    @transaction.atomic
    def post(self,request):
        try:
            email = username = request.data.get("email").strip()
            password = request.data.get("password")
            name = request.data.get("name")
            category = request.data.get("category")
            address = request.data.get("address")
            longitude = request.data.get("longitude")
            latitude = request.data.get("latitude")

            user = User.objects.filter(email=email).last()
            if user != None:
                return Response({"error" : 'Email already exists. Please enter another ID'.format(request.data.get("email"))},status=400)
            else:
                user = User.objects.create_user(
                    username, email, password, 
                )
            
                # user = authenticate(email=email, password=password)

                business = BusinessOwner()
                business.user_id = user.id
                business.name = name
                business.category = category
                business.address = address
                business.latitude = latitude
                business.longitude = longitude
                business.save()

                response = {
                            'success': 'True',
                            'message': 'User logged in successfully',
                            'user_email': user.email,
                            'business_name': business.name,
                            'business_category': business.category,
                            'business_address': business.address,
                            'business_latitude': business.latitude,
                            'business_longitude': business.longitude,
                            'user_id': user.id,
                            'business_id': business.id,
                        }

                return Response(response,status=201)
        except Exception as e:
            print(traceback.format_exc())
            return Response({'errorNeel': '{}'.format(e)},status=400)


class LoginBusiness(generics.GenericAPIView):
    def post(self,request):
        try:
            username = request.data.get("email",None)
            password = request.data.get("password",None)
            # print(username)
            loginCheck = authenticate(username=username, password=password)
            print(loginCheck)
            if loginCheck is None:
                business_email = User.objects.filter(username=username).first()
                if business_email is None:
                    return Response({"error":'User with this email and password is not found'})
                else:
                    return Response({"error":'Incorrect Password'})
            else:
                response= {
                        'success': 'True',
                        'message':'User logged In successfully',
                    }
                return Response(response,status=201)
        except Exception as e:
            print(traceback.format_exc())
            return Response({'error': '{}'.format(e)},status=400)

