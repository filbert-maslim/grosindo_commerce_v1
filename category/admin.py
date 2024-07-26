from django.contrib import admin
from .models import CategoryLvlOne, CategoryLvlTwo, Category

# Register your models here.
class CategoryLvlOneAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')

class CategoryLvlTwoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')

admin.site.register(CategoryLvlOne, CategoryLvlOneAdmin)
admin.site.register(CategoryLvlTwo, CategoryLvlTwoAdmin)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')

admin.site.register(Category, CategoryAdmin)
