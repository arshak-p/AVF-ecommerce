from .models import CartItem,Cart

def cart_item_count(request):
    cart_item_count = 0

    if request.user.is_authenticated:
        cart_item_count = CartItem.objects.filter(user=request.user, is_active=True).count()
    else:
        cart = Cart.objects.get(session_id=_session_id(request))
        cart_item_count = CartItem.objects.filter(cart=cart, is_active=True).count()

    return {'cart_item_count': cart_item_count}