from django.shortcuts import render, redirect,get_object_or_404
from store.models import Product
from django.contrib import messages
from offers.models import Coupon
from .models import Cart,CartItem
from django.http import JsonResponse
# Create your views here.

def _session_id(request):
    cart = request.session.session_key

    # if user is not loggined
    if not cart:
        cart = request.session.create()
    return cart


# for adding products to the cart

# def add_cart(request, product_id):
#     product = Product.objects.get(id = product_id)
#     try:
#         # it will retreive existing cart
#         cart = Cart.objects.get(session_id=_session_id(request))
#     except Cart.DoesNotExist:
#         # if there is no cart  it will create a new cart
#         cart = Cart.objects.create(
#             session_id = _session_id(request)
#         )
   
#     cart.coupon = None
#     cart.save()

#     try:
#         # if the product already in the cart it will increase cart item quantity
#         cart_item = CartItem.objects.get(product=product, cart=cart)
#         if ((product.stock)-(cart_item.quantity + 1)) < 0:
#             messages.warning(request, "Out of stock")
#             return redirect('cart')
#         cart_item.quantity += 1
#         cart_item.save()
#     except CartItem.DoesNotExist:
#         if request.user.is_authenticated:
#             if ((product.stock)- 1) < 0:
#                 print('hi') 
#                 return redirect('cart')
#             cart_item = CartItem.objects.create(
#                 product = product,
#                 quantity = 1, 
#                 cart = cart,
#                 user = request.user,
#             )
#             cart_item.save()
#         else:
#             cart_item = CartItem.objects.create(
#                 product = product,
#                 quantity = 1, 
#                 cart = cart,
#             )
#             cart_item.save()
#     return redirect('cart')
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(session_id=_session_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(session_id=_session_id(request))
   
    cart.coupon = None
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if ((product.stock) - (cart_item.quantity + 1)) < 0:
            response_data = {
                'error': 'Out of stock',
            }
            return JsonResponse(response_data, status=400)
        
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        if request.user.is_authenticated:
            if ((product.stock) - 1) < 0:
                response_data = {
                    'error': 'Out of stock',
                }
                return JsonResponse(response_data, status=400)
                
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
                user=request.user,
            )
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            cart_item.save()

    cart_items = CartItem.objects.filter(cart=cart)
    total = 0
    for cart_item in cart_items:
        if cart_item.product.offer:
            total += cart_item.sub_total_with_offer()
        elif cart_item.product.category.offer:
            total += cart_item.sub_total_with_offer_category()
        else:
            total += cart_item.sub_total()

        subtotal = total

    response_data = {
        'subtotal': subtotal,
        'quantity': cart_item.quantity,
        'item_price': cart_item.product.price,
    }
    return JsonResponse(response_data)

# # for reducing cart item quantity
# def remove_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     cart = Cart.objects.get(session_id=_session_id(request))
#     cart.coupon = None
#     cart.save()
#     if request.user.is_authenticated:
#         cart_item = CartItem.objects.get(product=product, user=request.user)
#     else:
        
#         cart_item = CartItem.objects.get(product=product, cart=cart)
#     if cart_item.quantity > 1:
#         cart_item.quantity -= 1
#         cart_item.save()
#     else:
#         cart_item.delete()
#     return redirect('cart')


from django.http import JsonResponse

def remove_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(session_id=_session_id(request))
    cart.coupon = None
    cart.save()
    
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

        # Prepare the JSON response
        print('quantity is -------------------', cart_item.quantity)

        cart_items = CartItem.objects.filter(cart=cart)
        total = 0
        for cart_item in cart_items:
            if cart_item.product.offer:
                total += cart_item.sub_total_with_offer()
            elif cart_item.product.category.offer:
                total += cart_item.sub_total_with_offer_category()
            else:
                total += cart_item.sub_total()

            subtotal = total

        response_data = {
            'subtotal': subtotal,
            'quantity': cart_item.quantity,
            # 'cart_total': cart.total(),  # Update this according to your cart calculation logic
            'item_price': cart_item.product.price,  # Update this according to your cart item price calculation
        }
        return JsonResponse(response_data)
        
    except CartItem.DoesNotExist:
        # Handle the case where the cart item does not exist
        response_data = {
            'error': 'Cart item not found.',
        }
        return JsonResponse(response_data, status=400)




#for removing cart item 
def delete_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(session_id=_session_id(request))
    cart.coupon = None
    cart.save()
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user)
    else:
        cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')
                       

# For showing cart items on cart page 

def cart(request, total=0, quantity=0, cart_items=None,count=0,coupons=None, cart=None,discount_amount=0, subtotal=0):

    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True).order_by('-id')
            coupons = Coupon.objects.all()
        else:
            cart = Cart.objects.get(session_id = _session_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            
        for cart_item in cart_items:
            if cart_item.product.offer:
                total += cart_item.sub_total_with_offer()
            elif cart_item.product.category.offer:
                total += cart_item.sub_total_with_offer_category()
            else:
                total += cart_item.sub_total()

            quantity += cart_item.quantity
            count += 1
            subtotal = total
        
       
    except:
        pass

    # for adding coupons
    if request.method == "POST":
        coup = request.POST['search']
        try:
            coupon = Coupon.objects.get(coupon_code = coup)
            if coupon.is_expired():
                messages.error(request, 'Coupon is expired')
                return redirect('cart')
            
            if coupon.min_amount > total:
                messages.error(request, f'Amount should be greater than {coupon.min_amount}')
                return redirect('cart')
            
            cart = Cart.objects.get(session_id = _session_id(request))

            discount_amount = total * coupon.off_percent / 100

            if discount_amount > coupon.max_discount:
                discount_amount = coupon.max_discount

            subtotal = total
            total -= discount_amount

            cart.coupon = coupon
            cart.save()
                
        except:
            messages.error(request, 'Coupon not found')
            return redirect('cart')

    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'count': count,
        'coupons': coupons,
        'cart':cart,
        'discount_amount':discount_amount,
        'sub_total':subtotal,
    }

    return render(request, "cart.html", context)

