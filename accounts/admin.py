from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserAddress

# Make password as read only and display selected fields
class AccountAdmin(UserAdmin):
    list_display = ('email','name', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email','name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
class UserAddressAdmin(admin.ModelAdmin):
    list_display=('user','street_address','is_verified')

admin.site.register(User, AccountAdmin)
admin.site.register(UserAddress, UserAddressAdmin)