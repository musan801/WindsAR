from django.urls import include,path
from .views import RegisterCustomerView,LoginCustomer,RegisterBusinessView,LoginBusiness,CustomerProfile


urlpatterns = [
    path('register/', RegisterCustomerView.as_view(), name='create-customer'),
    path('login/', LoginCustomer.as_view(), name='login-Customer'),
    path('loginBusiness/', LoginBusiness.as_view(), name='login-Business'),
    path('registerBusiness/', RegisterBusinessView.as_view(), name='create-business'),
    path('customerProfile/',CustomerProfile.as_view(),name='customer-profile'),
    
]


    
    