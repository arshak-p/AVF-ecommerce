from django.urls import path
from authapp import views

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('login/',views.handlelogin, name='handlelogin'),
    path('logout/',views.handlelogout, name='handlelogout'),
    path('forgotpassword/',views.forgot_password, name='forgotpassword'),
    path('resetpassword/',views.reset_password, name='resetpassword'),
    path('otp_login/',views.otp_login, name='otp_login'),
]

 

