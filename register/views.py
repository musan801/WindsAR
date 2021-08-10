from django.contrib.auth import models
from django.db.models import manager
from django.http import response
from django.shortcuts import render
from django.db import transaction

from django.contrib.auth.models import User
# Create your views here.
from .models import RegisterCustomer,MarkerLocations
from .models import Voucher
from django.db.models import F
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth import authenticate
import traceback
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny, NOT
from .models import BusinessOwner,MarkerLocations
from .serializers import CustomerSerializer, fetchVouchersSerializer
from .serializers import updateCoins
from .serializers import fetchAuthDetails
from rest_framework import status
from rest_framework import viewsets
from . import serializers
import datetime
import math
from django.http import JsonResponse
from .serializers import BusinessOwnerSerializer, fetchAllLocationSerializers
import json
from rest_framework.views import APIView

class RegisterCustomerView(generics.GenericAPIView):
    @transaction.atomic
    def post(self,request):
        try:
            email = username = request.data.get("email").strip()
            password = request.data.get("password")
            name = request.data.get("name")
            dob = request.data.get('dob')       
            # dob format yyyy-mm-dd

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
                print("***********************")
                print(cusID)
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
            email = username = request.data.get("email")
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
                queryset = BusinessOwner.objects.filter(user_id=loginCheck.id).last()
                getData = BusinessOwnerSerializer(queryset,many=False)
                cusID = getData.data
                print(cusID)
                print(cusID.get('name'))
                print(cusID.get('user'))

                response= {
                        'success': 'True',
                        'message':'User logged In successfully',
                        'user_id' : cusID.get('user'),
                        'BusinessName' : cusID.get('name'),
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
                'success' : 'true',
                'name': jsonData.get('name'),
                'age' : age,
                'winCoins': jsonData.get('winCoins'),
                'placeVisited' : jsonData.get('placesVisited'),
                'vouchers' : jsonData.get('vouchers'),
                'email': authUserdata.get('email'),
            }

            return Response(response,status=201)

        except Exception as e:
            print(traceback.format_exc())
            return Response({'error': '{}'.format(e)},status=400)


class updateCoinsAndPlaces(generics.GenericAPIView):
    def post(self,request):
        try:
            id = request.data.get('id',None)
            user_id = request.data.get('user_id',None)
            winCoins = request.data.get('winCoins',None)
            print(id)
            queryset = RegisterCustomer.objects.filter(user_id=user_id).last()
            queryset.winCoins += int(winCoins)
            queryset.placesVisited += 1
            queryset.save()

            placeName = request.data.get('placeName',None)
            locationLatitude = request.data.get('locationLatitude',None)
            locationLongitude = request.data.get('locationLongitude',None)
            
            addHistory = PlacesHistory()
            addHistory.placeName = placeName
            addHistory.locationLatitude = locationLatitude
            addHistory.locationLongitude = locationLongitude
            addHistory.registerCustomer_id = id
            addHistory.save()

            response = {
                'success' : 'true',
                'message' : 'Values updated'
            }
            return Response(response,status=201)
        except Exception as e:
            print(traceback.format_exc())
            return Response({'error': '{}'.format(e)},status=400)


class addVoucher(generics.GenericAPIView):
    
    def post(self,request):
        try:
            def CalcCoins(ActualPrice,DiscPrice):
                #calc perent disc
                Perc= ((ActualPrice-DiscPrice)/ActualPrice)*100
                #cash disc
                CashOff=ActualPrice-DiscPrice
                perc = int(Perc)
                cashOff = int(CashOff)
                return int(perc*cashOff*4)

            businessName = request.data.get('businessName',None)
            productName = request.data.get('productName',None)
            discountPrice = request.data.get('discountPrice',None)
            expiryDate = request.data.get('expiryDate',None)
            # date format yyyy-mm-dd
            
            actualPrice = request.data.get('actualPrice',None)

            winCoins = CalcCoins(int(actualPrice),int(discountPrice))
            print(winCoins)

            add = Voucher()
            add.businessName = businessName
            add.productName = productName
            add.discountPrice = discountPrice
            add.expiryDate = expiryDate
            add.actualPrice = actualPrice
            add.winCoins = winCoins
            add.save()

            response = {
                'success' : 'true',
                'message' : 'Voucher is added successfully',
                'businessName' : add.businessName,
                'productName' : add.productName,
                'discountPrice' : add.discountPrice,
                'expiryDate' : add.expiryDate,
                'actualPrice' : add.actualPrice,
                'winCoins' : add.winCoins
            }
            return Response(response,status=201)
        except Exception as e:
            print(traceback.format_exc())
            return Response({'error': '{}'.format(e)},status=400)


class fetchAllVouchersCustomer(generics.GenericAPIView):
    def post(self,request):
        try:
            queryset = Voucher.objects.all()
            getAllData = fetchVouchersSerializer(queryset,many=True)
            jsonData = getAllData.data
            # winCoins = json.get('winCoins')
            
            id = request.data.get('id',None)
            queryset2 = RegisterCustomer.objects.filter(user_id=id).last()
            getData = CustomerSerializer(queryset2,many=False)
            jsonData2 = getData.data

            winCoins = jsonData2.get('winCoins')
            
            return Response(json.dumps(jsonData),status=201)
        except Exception as e:
            print(traceback.format_exc())
            return Response({'error': '{}'.format(e)},status=400)

class addMarkerLocation(generics.GenericAPIView):
    def post(self,request):
        try:
            def CalcCoinsTour(Rating,Review):
                Rating = float(Rating)
                Review = int(Review)
                print(Rating)
                print(Review)
                Total = (Rating*Review/Review+Rating*2)+(Review/2) + (Rating*1000)+200
                if Review >100:

                    Total= Total/30
                else:
                    Total/= 50
                    Total=50 *round(Total/50)
                    
                return math.ceil(Total)

            name = request.data.get('name',None)
            Lat = request.data.get('Lat',None)
            Long = request.data.get('Long',None)
            description = request.data.get('description',None)
            review = request.data.get('review',None)
            imagelink = request.data.get('imagelink',None)
            rating = request.data.get('rating',None)
            address = request.data.get('address',None)

            winCoins = CalcCoinsTour(float(rating),float(review))
            
            addMarker = MarkerLocations()
            addMarker.name = name
            addMarker.Lat = Lat
            addMarker.Long = Long
            addMarker.description = description
            addMarker.address = address
            addMarker.imagelink=imagelink
            addMarker.winCoins = winCoins
            addMarker.save()
            
            response={
                'success':'true',
                'message':'successfully',
                'name' : name,
                'Lat' : Lat,
                'Long' : Long,
                'description' : description,
                'address' : address,
                'winCoins' : winCoins,
                'imagelink' : imagelink,
            }
            return Response(response,status=201)
        except Exception as e:
            print(traceback.format_exc())
            return Response({'error':'{}'.format(e)},status=400)

class fetchMarkerLocation(generics.GenericAPIView):
    def post(self,request):
        try:
            queryset = MarkerLocations.objects.all()
            getAllData = fetchAllLocationSerializers(queryset,many=True)
            jsonData = getAllData.data
            
            return Response(getAllData.data,status=201)
        except Exception as e :
            print(traceback.format_exc())
            return Response({'error':'{}'.format(e)},status=400)

class userEditProfile(generics.GenericAPIView):
    def post(self,request):
        try:
            id = request.data.get('id',None)
            email = request.data.get('email',None)
            name = request.data.get('name',None)

            queryset = RegisterCustomer.objects.filter(user_id=id).last()
            queryset.name = name
            queryset.user.email = email
            queryset.save()
            
            response = {
                'success' : 'True',
                'message':'Successfully edited Customer profile'
            }
            return Response(response,status=201)
        except Exception as e:
            print(traceback.format_exc())
            return Response({'error':'{}'.format(e)},status=400)

class businessEditProfile(generics.GenericAPIView):
    def post(self,request):
        try:
            id = request.data.get('id',None)
            name = request.data.get('name',None)
            email = request.data.get('email',None)

            queryset = BusinessOwner.objects.filter(user_id=id).last()
            queryset.name = name
            queryset.email = email
            queryset.save()

            response = {
                'success' : 'True',
                'message':'Successfully edited Customer profile'
            }
            return Response(response,status=201)
        except Exception as e:
            print(traceback.format_exc())
            return Response({'error':'{}'.format(e)},status=400)

class deleteVoucher(APIView):
    
    def delete(self,request):
            try:
                id = request.data.get('id',None)
                queryset = Voucher.objects.filter(user_id = id)
                queryset.delete()
                return Response('Voucher Deleted')
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

class redeemVoucher(generics.GenericAPIView):
    def post(self,request):
        try:
            user_id = request.data.get('user_id',None)
            voucherWinCoins = request.data.get('winCoins',None)

            queryset = RegisterCustomer.objects.filter(user_id=user_id).last()
            queryset.winCoins -= int(voucherWinCoins)
            queryset.save()

            response = {
                'success' : 'True',
                'message' : 'successfully done',
                'winCoins' : queryset.winCoins
            }
            return Response(response,status=201)
        except Exception as e:
            print(traceback.format_exc())
            return Response({'error':'{}'.format(e)},status=400)


