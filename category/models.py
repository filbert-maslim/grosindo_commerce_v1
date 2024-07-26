from django.db import models
from django.urls import reverse

# generate path from the slug field
def get_path(instance, filename):
    return 'categories/photos/{}/{}'.format(instance.slug, filename)

# Category model
class CategoryLvlOne(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    descriptions = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to=get_path, blank=True)
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'category_lvl_one'

    def get_url(self):
        return reverse('products_by_category_lvl_one', args=[self.slug])
    
    def __str__(self):
        return self.category_name
    
class CategoryLvlTwo(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    category_lvl_one = models.ForeignKey(CategoryLvlOne, on_delete=models.CASCADE, null=False)
    slug = models.CharField(max_length=100, unique=False)
    descriptions = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to=get_path, blank=True)
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'category_lvl_two'

    def get_url(self):
        return reverse('products_by_category_lvl_two', args=[self.slug])
    
    def __str__(self):
        return self.category_name
    
# Category model
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    descriptions = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to=get_path, blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])
    
    def __str__(self):
        return self.category_name