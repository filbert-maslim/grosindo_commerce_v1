from django.shortcuts import render
from products.models import Product
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
def store(request):
    products = Product.objects.filter(is_acitve=True)

    paginator = Paginator(products, 1)
    page = request.GET.get('page')
    paged_products=paginator.get_page(page)
    products_count = products.count()

    context={
        'products':paged_products,
        'products_count':products_count,
    }
    return render(request, 'store/store.html', context)

def search(request):
    products = None
    products_count = 0
    keyword = None
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']

    if keyword:
        products = Product.objects.filter(Q(description__icontains=keyword)|Q(product_name__icontains=keyword))
        products_count = products.count()

        context={
            'products':products,
            'products_count':products_count,
        }

    else:
        products = Product.objects.filter(is_active=True)

        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products=paginator.get_page(page)
        products_count = products.count()

        context={
            'products':paged_products,
            'products_count':products_count,
        }

    return render(request, 'store/store.html', context)