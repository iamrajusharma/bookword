from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
# import methods and classes from views.py 
from .views import *

from .checkoutpayment import CheckoutPage

from .payment import PaymentCreated,verify_payment,addresspage,OrderDonePage
urlpatterns = [
    path('',index,name="index"),
    path('add/login/',LoginView.as_view(template_name = "login.html"),name='login'),
    path('add/', add_product, name='add_product'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('clear_cart/<int:product_id>/',clear_cart,name='clear_cart'),
    path('logout/',LogoutView.as_view() ,name='logout'),
    path('registration/',registration,name='registration'),
    path('user_login/',user_login,name='user_login'),
    path('user_logout/',user_logout,name='user_logout'),


    # payment created file 
     path('PaymentCreated/<str:product_ids>/', PaymentCreated, name='PaymentCreated'),
    # other URLs
    # path('PaymentCreated/<int:product_id>/', PaymentCreated, name='PaymentCreated'),
    path('verify-payment/', verify_payment, name='verify_payment'),
    # addresspage
    path('addresspage/',addresspage,name='addresspage'),

    # order done page now 
    # OrderDonePage

    path('OrderDonePage/',OrderDonePage,name='OrderDonePage'),
    # check order

    path('OrderPage/',OrderPage,name='OrderPage'),


    # urls for add quantity in check out page 

    
    path('add_quantity/<int:product_id>/',add_quantity,name="add_quantity"),
    path('sub_quantity/<int:product_id>/',sub_quantity,name="sub_quantity"),


    # cart check out page 

    # CheckoutPage/



    path('CheckoutPage',CheckoutPage,name="CheckoutPage"),
   
]
