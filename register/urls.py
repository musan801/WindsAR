from django.urls import include,path
from .views import RegisterCustomerView,LoginCustomer,RegisterBusinessView,LoginBusiness,CustomerProfile,updateCoinsAndPlaces
from .views import addVoucher,fetchAllVouchersCustomer,addMarkerLocation,fetchMarkerLocation,userEditProfile,businessEditProfile

urlpatterns = [
    path('register/', RegisterCustomerView.as_view(), name='create-customer'),
    path('login/', LoginCustomer.as_view(), name='login-Customer'),
    path('loginBusiness/', LoginBusiness.as_view(), name='login-Business'),
    path('registerBusiness/', RegisterBusinessView.as_view(), name='create-business'),
    path('customerProfile/',CustomerProfile.as_view(),name='customer-profile'),
    path('updateCoins/',updateCoinsAndPlaces.as_view(),name='update-Coins'),
    path('addVoucher/',addVoucher.as_view(),name='add-voucher'),
    path('fetchVoucher/',fetchAllVouchersCustomer.as_view(),name='fetch-voucher'),
    path('addMarkerLocation/',addMarkerLocation.as_view(),name='add-MarkerLocation'),
    path('fetchMarkerLocation/',fetchMarkerLocation.as_view(),name='fetch-MarkerLocation'),
    path('userEditProfile/',userEditProfile.as_view(),name='user-EditProfile'),
    path('businessEditProfile/',businessEditProfile.as_view(),name='business-EditProfile'),

]

