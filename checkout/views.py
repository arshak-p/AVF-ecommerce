from django.shortcuts import redirect, render
from user_profile.models import UserAddress
from cart.models import *
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='handlelogin')
def checkout(request):
    total = 0 
    quantity = 0
    subtotal = 0
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        for cart_item in cart_items:
            if cart_item.quantity > cart_item.product.stock:
                    print("cart item out of stock")
                    return redirect('cart')
            total += cart_item.sub_total()
            quantity += cart_item.quantity
            subtotal = total
            

        address = UserAddress.objects.filter(user=request.user).order_by('-id').first() 
        context = {
            'addresses':address,
            'total' : total,
            'quantity' : quantity,
            'cart_items' : cart_items,  
            'sub_total':subtotal,

        }
    return render(request, "checkout.html", context)

