from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Product, Wishlist
from category.models import Category
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='handlelogin')
def wishlist(request):
    usr = request.user.id
    try:
        products = Wishlist.objects.filter(user=usr)
    except:
        products = ''
    return render(request, 'wishlist.html', {'wishlisted': products})


@login_required(login_url='handlelogin')
def add_wishlist(request, id):
    try:
        product = Product.objects.get(id=id)
    except Exception as e:
        raise e
    user = request.user
    try:
        wishlist = Wishlist.objects.get(user=user, product=product)
        messages.warning(request, "Item already added to favourite!")
    except Wishlist.DoesNotExist:
        wishlist = Wishlist(user=user,  product=product)
        wishlist.save()
        messages.success(request, 'Item added to wishlist')

    context = {'single_product': product}
    return render(request, 'single.html', context)


@login_required(login_url='handlelogin')
def delete_wishlist(request, id):
    usr = request.user.id
    product = Wishlist.objects.get(user=usr, product=id)
    product.delete()
    return redirect(wishlist)
