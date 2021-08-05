from django.contrib.auth import models
from django.db.models import manager
from django.http import response
from django.shortcuts import render
from django.db import transaction

from django.contrib.auth.models import User
# Create your views here.
from .models import RegisterCustomer
from django.db.models import F
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth import authenticate
import traceback
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny, NOT
from .models import BusinessOwner
from .serializers import CustomerSerializer
from .serializers import updateCoins
from .serializers import fetchAuthDetails
from rest_framework import status
from rest_framework import viewsets
from . import serializers
import datetime
from django.http import JsonResponse
import json

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
            print(loginCheck.id)
            if loginCheck is None:
                customer_email = User.objects.filter(username=username).first()
                
                if customer_email is None:
                    return Response({"error":'User with this email and password is not found'})
                else:
                    return Response({"error":'Incorrect Password'})
            else:
                print("**************")
                queryset = RegisterCustomer.objects.filter(user_id=loginCheck.id).last()
                getData = CustomerSerializer(queryset,many=False)
                cusID = getData.data
                print(cusID.get('name'))
                
                response= {
                        'success': 'True',
                        'message':'User logged In successfully',
                        # 'custome_name': cusID.get('name'),
                        # 'customer_dob': cusID.get('dob'),
                        'customer_name': cusID.get('name'),
                        'customer_id': loginCheck.id,
                        # 'customer_winCoins': cusID.get('winCoins'),
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


class CustomerProfile(generics.GenericAPIView):
    def post(self,request):
        try:
            id = request.data.get('id',None)
            queryset = RegisterCustomer.objects.filter(user=id).last()
            getAllData = CustomerSerializer(queryset,many=False)
            jsonData = getAllData.data
            print(jsonData)

            #convert dob from string datetime
            dob = jsonData.get('dob')
            updatedDOB = datetime.datetime.strptime(dob,'%Y-%M-%d').date()
            
            #calculate age from datetime
            today = datetime.date.today()
            age = today.year - updatedDOB.year - ((today.month, today.day) < (updatedDOB.month, updatedDOB.day))
            print(age)
            
            querysetAuth = User.objects.filter(id=id).last()
            getAllData2 = fetchAuthDetails(querysetAuth,many=False)
            authUserdata = getAllData2.data
            print("................................")
            print(authUserdata)
            
            response ={
                'name': jsonData.get('name'),
                'age' : age,
                'winCoins': jsonData.get('winCoins'),
                'placeVisited' : jsonData.get('placesVisited'),
                'vouchers' : jsonData.get('vouchers'),
                'email': authUserdata.get('email'),
            }

            return Response(response,status=201)
            # username:request.data.get('email',None)
            # queryset = RegisterCustomer.objects.filter(user=loginCheck.id).last()
            # getData = CustomerSerializer(queryset,many=False)
            # cusID = getData.data
            # print(cusID.get('name'))

        except Exception as e:
            print(traceback.format_exc())
            return Response({'error': '{}'.format(e)},status=400)


# class updateCoinsAndPlaces(generics.GenericAPIView):
    
#     def retrieve(self,request,*args,**kwargs):
#         try:
            
#             queryset = RegisterCustomer.objects.all()
#             serializer_class = CustomerSerializer

#             winCoins = request.data.get('winCoins',None)
#             print(winCoins)
#             instance = self.get_object()
#             RegisterCustomer.objects.filter(pk=instance.id).update(winCoins = F('winCoins')+ winCoins)
#             serializer = self.get_serializer(instance)
#             return JsonResponse(serializer.data)


#             # qs = RegisterCustomer.objects.filter(user =id).last()
#             # print(qs)
#             # serializer = CustomerSerializer(qs,data=winCoins,many=False)
#             # serializer.is_valid(raise_exception=True)
#             # # if serializer.is_valid:
#             # serializer.save()
            
#             # return Response(serializer.data)



#             # queryset = RegisterCustomer.objects.filter(user=id).last()
#             # getData = CustomerSerializer(queryset,many=False)
#             # jsonData = getData.data
            
#             # print(jsonData)
#             # print("*********************")
#             # instance = self.get_object()
#             # instance.winCoins = winCoins + jsonData.get('winCoins')
#             # instance.save()

#             # serializer = self.get_serializer(instance)
#             # serializer.is_valid(raise_exception=True)
#             # self.perform_update(serializer)
            

#             # print(serializer.data)





#             # queryset = RegisterCustomer.objects.filter(user=id).last()
#             # getAllData = CustomerSerializer(queryset,many=False)
#             # jsonData = getAllData.data

#             # print(jsonData)
#             # name = jsonData.get('name')
#             # id = jsonData.get('id')
#             # dob = jsonData.get('dob')
#             # placeVisited = jsonData.get('placesVisited')
#             # vouchers = jsonData.get('vouchers')
#             # user = jsonData.get('user')


#             # placeWinCoins = jsonData.get('winCoins')
#             # placeWinCoins = placeWinCoins + int(winCoins)

#             # placeVisited = placeVisited + 1
            
#             # customerCoins = RegisterCustomer()

#             # customerCoins.winCoins = placeWinCoins
#             # customerCoins.name = name
#             # customerCoins.dob = dob
#             # customerCoins.placesVisited = placeVisited
#             # customerCoins.vouchers = vouchers
#             # customerCoins.save()

#             # response={
#             #     'message': 'WinCoins Updated'
#             # }
#             # return Response(response,status=201)
#         except Exception as e:
#             print(traceback.format_exc())
#             return Response({'error': '{}'.format(e)},status=400)
