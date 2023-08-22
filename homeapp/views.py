from django.shortcuts import render
from category.models import Brand
from category.models import Category
from store.models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from user_profile.models import Wallet, WalletTransaction
# Create your views here.


def shop(request):
    current_pages = "shop"
    brand = Brand.objects.filter(is_available=True)
    category = Category.objects.filter(is_available=True)
    product = Product.objects.filter(is_available=True)
    per_page = 4

    page_number = request.GET.get('page')
    paginator = Paginator(product, per_page)
    try:
        current_page = paginator.page(page_number)

    except PageNotAnInteger:
        current_page = paginator.page(1)

    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
    context = {
        'brand': brand,
        'categorys': category,
        'current_page': current_page,
        'products': product,
        'current_pages': current_pages,

    }

    return render(request, "shop.html", context)


def index(request):
    current_page = "index"
    brands = Brand.objects.filter(is_available=True)
    context = {
        'brands': brands,
        'current_page': current_page,

    }
    return render(request, "index.html", context)


def cart(request):
    current_page = "cart"
    return render(request, "cart.html", {'current_page': current_page})


def product(request):
    current_page = "product"
    product = Product.objects.filter(is_available=True)
    context = {
        'products': product,
        'current_page': current_page,

    }
    return render(request, "single.html", context)


def wallet(request):
    wallet, _ = Wallet.objects.get_or_create(user=request.user)
    transactions = WalletTransaction.objects.filter(wallet=wallet)
    context = {'wallet': wallet}
    if transactions.exists():
        context['transactions'] = transactions

    return render(request, "wallet.html", context)
