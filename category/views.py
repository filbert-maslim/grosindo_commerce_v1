from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator


from .models import CategoryLvlOne, CategoryLvlTwo
from products.models import Product
# Create your views here.

def CategoryLvlOne(request, category_lvl_one_slug=None):
    if category_lvl_one_slug:
        categories = get_object_or_404(CategoryLvlOne, slug=category_lvl_one_slug)
        products = Product.objects.filter(category_lvl_one=categories, is_active=True)
        products_count = products.count()
    else:
        products = Product.objects.filter(is_active=True)

    paginator = Paginator(products, 30)
    page = request.GET.get('page')
    paged_products=paginator.get_page(page)
    products_count = products.count()

    context={
        'products':paged_products,
        'products_count':products_count,
    }
    
    return render(request, 'store/store.html', context)

def CategoryLvlTwo(request, category_lvl_one_slug=None, category_lvl_two_slug=None):
    if category_lvl_two_slug:
        category_lvl_two = get_object_or_404(CategoryLvlTwo, category_lv_one__slug=category_lvl_one_slug,
                                             slug=category_lvl_two_slug, )
        products = Product.objects.filter(category_lvl_two=category_lvl_two, is_active=True)
        products_count = products.count()
    else:
        products = Product.objects.filter(is_active=True)

    paginator = Paginator(products, 30)
    page = request.GET.get('page')
    paged_products=paginator.get_page(page)
    products_count = products.count()

    context={
        'products':paged_products,
        'products_count':products_count,
    }
    
    return render(request, 'store/store.html', context)