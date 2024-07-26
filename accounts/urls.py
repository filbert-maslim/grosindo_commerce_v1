from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('address/', views.AddressList, name='user_address'),
    path('address/new', views.NewAddress, name='new_address'),
    path('address/update/<int:address_id>', views.UpdateAddress, name='update_address'),
    path('address/delete/<int:address_id>', views.DeleteAddress, name='delete_address'),
]