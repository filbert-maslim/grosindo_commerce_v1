from allauth.account.adapter import DefaultAccountAdapter # type: ignore
from cart.models import Cart, CartItem
from cart.views import _cart_id
from django.contrib.auth import authenticate

class AccountAdapter(DefaultAccountAdapter):
    # Modify allauth default account adapter to automatically merge users' cart upon authentication
    def authenticate(self, request, **credentials):
        from allauth.account.auth_backends import AuthenticationBackend # type: ignore

        self.pre_authenticate(request, **credentials)
        AuthenticationBackend.unstash_authenticated_user()
        user = authenticate(request, **credentials)
        alt_user = AuthenticationBackend.unstash_authenticated_user()
        user = user or alt_user
        if user:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                
                if is_cart_item_exists:
                    user_cart_item = CartItem.objects.filter(user=user)
                    cart_item = CartItem.objects.filter(cart=cart)
                    existing_var_id=[list(item.variations.all()) for item in user_cart_item]
                    existing_cartitem_id = [item.id for item in user_cart_item]
                    
                    for item in cart_item:
                        var_id = list(item.variations.all())
                        if var_id in existing_var_id:
                            index=existing_var_id.index(var_id)
                            item_id = existing_cartitem_id[index]
                            existing_cartitem = CartItem.objects.get(id=item_id)
                            existing_cartitem.quantity += item.quantity
                            existing_cartitem.user = user
                            existing_cartitem.save()
                            item.delete()
                        else:
                            item.user = user
                            item.save()
                    
            except Exception as e:
                pass
            
            self._delete_login_attempts_cached_email(request, **credentials)
        else:
            self.authentication_failed(request, **credentials)
        return user
    
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        user.phone_number = data['phone_number']
        user.email = data['email']
        user.name = data['name']
        if 'password1' in data:
            user.set_password(data['password1'])
        else:
            user.set_unusable_password()
        # self.populate_username(request, user)
        if commit:
            user.save()
        return user