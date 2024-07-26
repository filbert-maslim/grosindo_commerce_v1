from django.db import models
from category.models import CategoryLvlOne, CategoryLvlTwo
from django.urls import reverse
from PIL import Image
from django.conf import settings

class Product(models.Model):
    product_name = models.CharField(max_length=250, unique = True)
    product_sku = models.CharField(max_length=10)
    slug = models.SlugField(max_length = 200, unique = True)
    category_lvl_one = models.ForeignKey(CategoryLvlOne, on_delete=models.SET_NULL, null=True)
    category_lvl_two = models.ForeignKey(CategoryLvlTwo, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length = 500, blank = True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True)
    last_modified_date = models.DateField(auto_now=True)

    class Meta:
        verbose_name = ("Product")
        verbose_name_plural = ("Products")

    def get_url(self):
        return reverse('product_detail', args=[self.slug])

    def __str__(self):
        return self.product_name
    
# generate path from the slug field
def product_image_path(instance , filename):
    return 'product/photos/{}/{}'.format(instance.product.slug, filename)

class ProductEcommerceUrl(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    url=models.URLField(max_length=200, null=True)
    platform=models.CharField(max_length=10, choices=settings.ECOMMERCE_PLATFORM, default='Shopee')
    craeted_at=models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('product', 'platform')
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    image = models.ImageField(upload_to = product_image_path)
    is_main = models.BooleanField(default=False, null=False)
    is_active = models.BooleanField(default=True, null=False)
    create_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
       instance = super(ProductImage, self).save(*args, **kwargs)
       image = Image.open(instance.image.path)
       image.save(instance.image.path, quality=75, optimize=True)
       return instance

# generate path from the slug field
def variation_image_path(instance , filename):
    return 'product/photos/{}/{}/{}'.format(instance.product.slug, instance.variation_sku, filename)

class Variation(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_name = models.CharField(max_length=100)
    variation_sku = models.CharField(max_length=10)
    price = models.IntegerField(null=False)
    bulk_disc = models.FloatField(null=True, default=0)
    wholesale_disc = models.FloatField(null=True, default=0)
    color = models.CharField(max_length=15, default='Random')
    size = models.FloatField(null=True, default=0)
    image = models.ImageField(upload_to=product_image_path, null=True)
    stock = models.IntegerField(default=0)
    weight = models.IntegerField(null=False)
    height = models.IntegerField(null=False)
    length = models.IntegerField(null=False)
    width = models.IntegerField(null=False)
    is_active = models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True)
    
    def get_volume(self):
        return self.width * self.length * self.height

    def __unicode__(self):
        return self.product