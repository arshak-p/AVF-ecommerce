from django.urls import path
from homeapp import views

urlpatterns = [
    path('',views.index,name="index"),
    path('shop',views.shop,name="shop"),
    path('cart',views.cart,name="cart"),
    path('product',views.product,name="product"),
    path('wallet',views.wallet,name="wallet")
]
   
  