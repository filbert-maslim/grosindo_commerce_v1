from django.shortcuts import render
from .models import Product
from cart.models import CartItem
from cart.views import _cart_id


# Create your views here.
def product_detail(request, product_slug):
    try:
        single_product = Product.objects.get(slug=product_slug)
        if request.user.is_authenticated:
            in_cart = CartItem.objects.filter(user=request.user, product=single_product).exists()
        else:
            in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
        context={
            'single_product':single_product,
            'in_cart':in_cart,
        }
    except Exception as e:
        raise e
    
    return render(request, 'store/product_detail.html', context)