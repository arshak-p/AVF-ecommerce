from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def adminpanel(request):
    
    return render(request,"adminpanel/index.html")

def signout(request):
    logout(request)
    return HttpResponseRedirect("/")

def user_details(request):
    if not request.user.is_authenticated and not request.user.is_superuser:
        return redirect('adminpanel')
    usr = User.objects.all()  
    context = {

        'users' : usr
    }
    return render(request, 'adminpanel/user.html', context)
def user_action(request, id):
    usr = User.objects.get(id=id)
    if usr.is_active:
        usr.is_active = False
        usr.save()
        return redirect(user_details)
    else:
        User.objects.get(id=id)
        usr.is_active = True
        usr.save()  
        return redirect(user_details)


def search_users(request):  
    search_text = request.POST['query']
    context = {
        'users': User.objects.filter(username__icontains=search_text),
        'search_text':search_text,
    }
    return render(request,'adminpanel/user.html',context)