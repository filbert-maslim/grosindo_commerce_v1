from django.db import models
from store.models import Product, Variation
from accounts.models import User

# Create your models here.
class Cart(models.Model):

    cart_id = models.CharField(max_length=250, blank=True)
    date_add = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = ("Cart")
        verbose_name_plural = ("Carts")

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations=models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = ("CartItem")
        verbose_name_plural = ("CartItems")

    def __unicode__(self):
        return self.product

