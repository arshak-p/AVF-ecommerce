from django.shortcuts import render
from .models import Product
from .models import Product, Brand
from category.models import Category
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger

# Create your views here.
def store(request):
    products = Product.objects.all().filter(is_available = True)
    per_page = 4
    page_number = request.GET.get('page')
    paginator = Paginator(products,per_page)
    try:
        current_page = Paginator(products,per_page)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
    context = {
        'current_page':current_page,
        'products' : products,
        
    }
    return render(request, 'shop.html', context)

def product_details(request, id):
    try:
        single_product = Product.objects.get(id = id)
    except Exception as e:
        raise e
    
    context = {
        'single_product' : single_product
    }
    return render(request, 'single.html', context)

def filtered_products(request):
    # Retrieve the filter options selected by the user from the URL query parameters
    selected_categories = request.GET.getlist('category')
    selected_brands = request.GET.getlist('brand')
    search_query = request.GET.get('q')


    # Query the database to get the filtered products
    filtered_products = Product.objects.filter(is_available = True)
    count = 0
    c = 0
    if search_query:
        count += 1
        filtered_products = filtered_products.filter(
            Q(product_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
        c = filtered_products.count()
    if selected_categories:
        filtered_products = filtered_products.filter(category__in=selected_categories)
        c = filtered_products.count()
        count += 1

    if selected_brands:
        filtered_products = filtered_products.filter(brand__in=selected_brands)
        count += 1
        c = filtered_products.count()
    
    if count == 0:
        filtered_products = None

    


    categories = Category.objects.all()
    brand = Brand.objects.all()

    context = {
        'products' : filtered_products,
        'categories' : categories,
        'brands' : brand,
        'c' : c,
        'f': True,
    }

    return render(request, 'shop.html', context)
