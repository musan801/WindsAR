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
from rest_framework.permissions import AllowAny

class RegisterCustomerView(generics.GenericAPIView):
    @transaction.atomic
    def post(self,request):
        try:
            email = username = request.data.get("email").strip()
            password = request.data.get("password")
            name = request.data.get("name")
            dob = request.data.get('dob')
            
            user = User.objects.filter(email=email).last()
            if user != None:
                return Response({"error" : 'Email already exists. Please enter another ID'.format(request.data.get("email"))},status=400)
            else:
                user = User.objects.create_user(
                    username, email, password,
                )
                
                # user = authenticate(email=email, password=password)

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
            print(username)
            loginCheck = authenticate(username=username, password=password)
            print(loginCheck)
            if loginCheck is None:
                customer_email = User.objects.filter(username=username).first()
                if customer_email is None:
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
