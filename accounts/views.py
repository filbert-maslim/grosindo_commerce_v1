from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404

from django.conf import settings
from .forms import AddressForm
from .models import UserAddress

@login_required(login_url = 'account_login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

@login_required(login_url = 'account_login')
def AddressList(request):
    user = request.user
    try:
        user_address = UserAddress.objects.filter(user=user, is_active=True)
        cnt_address = user_address.count()

    except ObjectDoesNotExist:
        user_address = None
        cnt_address = 0

    context={
        'user':user,
        'user_address':user_address,
        'cnt_address': cnt_address,
        }
    return render(request, 'accounts/address.html', context)

@login_required(login_url = 'account_login')
def NewAddress(request):
    user = request.user
    try:
        cnt_address = UserAddress.objects.filter(user=user, is_active=True).count()
    except ObjectDoesNotExist:
        cnt_address = 0
        
    if cnt_address >= settings.MAX_USER_ADDRESS_CNT:
        raise ValidationError('max number of address reached')
        
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            data = UserAddress()
            data.user = user
            data.address_name = form.cleaned_data['address_name']
            data.street_address = form.cleaned_data['street_address']
            data.contact_number = form.cleaned_data['contact_number']
            data.postal_code = form.cleaned_data['postal_code']
            data.ADMINISTRATIVE_AREA_LEVEL_1 = form.cleaned_data['ADMINISTRATIVE_AREA_LEVEL_1']
            data.ADMINISTRATIVE_AREA_LEVEL_2 = form.cleaned_data['ADMINISTRATIVE_AREA_LEVEL_2']
            data.ADMINISTRATIVE_AREA_LEVEL_3 = form.cleaned_data['ADMINISTRATIVE_AREA_LEVEL_3']
            data.ADMINISTRATIVE_AREA_LEVEL_4 = form.cleaned_data['ADMINISTRATIVE_AREA_LEVEL_4']
            if cnt_address < 1:
                data.is_main = True
            else:
                data.is_main = form.cleaned_data['is_main']
                
            data.save()
            
            return redirect('user_address')
    else:
        form = AddressForm()
        
    context = {
        'form':form,
        'cnt_address': cnt_address,
    }        
    return render(request, 'accounts/new_address.html', context)

@login_required(login_url = 'account_login')
def UpdateAddress(request, address_id=None):
    user = request.user
    if address_id:
        address = get_object_or_404(UserAddress, pk=address_id,)
        if address.user != user:
            return HttpResponseForbidden()
    else:
        return Http404()
    
    main_address = UserAddress.objects.filter(user=user, is_main=True)
     
    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('user_address')
    else:
        form = AddressForm(instance=address)  
         
    context = {
        'form':form,
        'address_id':address_id,
        'have_main_address':main_address.exists(),
    }        
    return render(request, 'accounts/new_address.html', context)

@login_required(login_url = 'account_login')
def DeleteAddress(request, address_id=None):
    user = request.user
    
    if address_id:
        address = get_object_or_404(UserAddress, id=address_id)
        if address.user != user:
            return HttpResponseForbidden()
        else:
            address.delete()
    
    return redirect('user_address')

@login_required(login_url = 'account_login')
def DeactivateAddress(request, address_id=None):
    user = request.user
    
    if address_id:
        address = get_object_or_404(UserAddress, id=address_id)
        if address.user != user:
            return HttpResponseForbidden()
        else:
            address.is_main = False
            address.is_active = False
            address.save()
    
    return redirect('user_address')