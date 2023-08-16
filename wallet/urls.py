from . import views
from django.urls import path 


urlpatterns = [
    path('my_wallet/',views.my_wallet, name='wallet'),
]
