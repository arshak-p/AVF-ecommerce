from . import views
from django.urls import path 

urlpatterns = [
    path('',views.cart, name='cart'),
    path('addcart/<int:product_id>/',views.add_cart, name='addcart'),
]
