from django import forms
from phonenumber_field.formfields import PhoneNumberField
from allauth.account.forms import SignupForm # type: ignore

from .models import User, UserAddress

class AllauthRegistrationForm(SignupForm):
    # Modify Allauth registration from to remove user name and ask for phone number
    class Meta:
        model = User
        fields = ['name', 'phone_number', 'email', 'password']   
    def __init__(self, *args, **kwargs):
        super(AllauthRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(required=True)
        self.fields['phone_number'] = PhoneNumberField(required=True)
        del self.fields["username"]
    def save(self, request):
        user = super(AllauthRegistrationForm, self).save(request)
        user.name = self.cleaned_data['name']
        user.phone_number = self.cleaned_data['phone_number']
        user.save()
        return user
    
class AddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ["address_name","street_address","contact_number","ADMINISTRATIVE_AREA_LEVEL_1",
                  "ADMINISTRATIVE_AREA_LEVEL_2","ADMINISTRATIVE_AREA_LEVEL_3","ADMINISTRATIVE_AREA_LEVEL_4",
                  "postal_code","notes","is_main","latitude", "longitude"]