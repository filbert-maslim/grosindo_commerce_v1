from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField

class MyAccountManager(BaseUserManager):
    # function to create normal users
    def create_user(self, name, phone_number, email, password=None):
        if not email:
            raise ValueError('Email address is required')
        if not phone_number:
            raise ValueError('Phone number is required')

        user = self.model(
            email = self.normalize_email(email),
            phone_number = phone_number,
            name = name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # function to create super users
    def create_superuser(self, name, email, phone_number, password):
        user = self.create_user(
            email = self.normalize_email(email),
            phone_number = phone_number,
            password=password,
            name = name,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

# User account model
class User(AbstractBaseUser):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254, unique=True)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_superadmin = models.BooleanField(default = False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name','email']

    objects = MyAccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    address_name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=150)
    contact_number = PhoneNumberField(null=False, blank=False)
    street_address = models.CharField(max_length=300, null=False)
    ADMINISTRATIVE_AREA_LEVEL_4 = models.CharField(max_length=50, null=False)
    ADMINISTRATIVE_AREA_LEVEL_3 = models.CharField(max_length=50, null=False)
    ADMINISTRATIVE_AREA_LEVEL_2 = models.CharField(max_length=50, null=False)
    ADMINISTRATIVE_AREA_LEVEL_1 = models.CharField(max_length=25, null=False)
    postal_code = models.IntegerField(null=False)
    notes = models.CharField(max_length=300, default=None, blank=True, null=True)
    latitude = models.FloatField(default=None, null=True, blank=True)
    longitude = models.FloatField(default=None, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_main = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'street_address')
    
    def __str__(self):
        return self.address_name
