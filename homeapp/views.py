from django.shortcuts import render
from category.models import Brand
from category.models import Category
from store.models import Product
from django.core.paginator import EmptyPage
# Create your views here.

def shop(request):
    current_page = "shop"
    brand = Brand.objects.filter(is_available = True)
    category = Category.objects.filter(is_available= True)
    product = Product.objects.filter(is_available = True)
    context = {
        'brand':brand,
        'categorys':category,
        'current_page':current_page,
        'products':product,

        }
    
    return render(request,"shop.html",context)

def index(request):
    current_page = "index"
    brands = Brand.objects.filter(is_available = True)
    context = {
        'brands':brands,
        'current_page':current_page,

        }
    return render(request, "index.html", context)

def cart(request):
    current_page = "cart"
    return render(request,"cart.html",{'current_page':current_page})

def product(request):
    current_page = "product"
    product = Product.objects.filter(is_available = True)
    context = {
        'products':product,
        'current_page':current_page,

        }
    return render(request,"single.html",context)
    