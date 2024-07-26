from django.shortcuts import render, redirect
from cart.models import CartItem
from .forms import OrderForm
from .models import Order, OrderProduct
from cart.models import Product
import datetime

# Create your views here.
def place_order(request):
    current_user = request.user
    
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <=0:
        return redirect('store')
    
    quantity=0
    total = 0
    
    for cart_item in cart_items:
        quantity += cart_item.quantity
        total += (cart_item.product.price * cart_item.quantity)
        
    tax=total*0.11
    grand_total = total+tax
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = request.user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address = form.cleaned_data['address']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            
            # generate order id
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
            }
            return render(request, 'orders/payments.html', context)
        # else:
        #     return redirect('checkout')
    else:        
        return render(request, 'orders/orders.html')
    
def payments(request, order_number):
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)
    order.is_ordered = True
    order.save()
    
    cart_items = CartItem.objects.filter(user=request.user)
    
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()
               
        orderproduct.variations.set(item.variations.all())
        orderproduct.save()
        
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
        
    cart_items.delete()
    
    return redirect('home')