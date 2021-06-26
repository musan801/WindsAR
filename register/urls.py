from django.urls import include,path
from .views import RegisterCustomerView,LoginCustomer


urlpatterns = [
    path('register/', RegisterCustomerView.as_view(), name='create-customer'),
    path('login/', LoginCustomer.as_view(), name='login-Customer'),
]
