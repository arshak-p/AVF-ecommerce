from django.shortcuts import render


# Create your views here.

def my_wallet(request):
    return render(request,'wallet.html')