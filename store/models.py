from django.db import models
from category.models import Category
from django.urls import reverse

# generate path from the slug field
def get_path(instance, filename):
    return 'product/photos/{}/{}'.format(instance.slug, filename)

class Product(models.Model):
    product_name = models.CharField(max_length=50, unique = True)
    slug = models.SlugField(max_length = 200, unique = True)
    description = models.TextField(max_length = 500, blank = True)
    price = models.IntegerField()
    images = models.ImageField(upload_to = get_path)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = ("Product")
        verbose_name_plural = ("Products")

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

class VariationManager(models.Manager):
    def color(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)
    def size(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)

class Variation(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=10, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True)

    objects = VariationManager()

    def __unicode__(self):
        return self.product
