from django.urls import path
from . import views

urlpatterns = [
    path('<slug:category_lvl_one_slug>/', views.CategoryLvlOne, name='cat_lvl_1'),
    path('<slug:category_lvl_one_slug>/<slug:category_lvl_two_slug>/', views.CategoryLvlTwo, name='cat_lvl_2'),
]