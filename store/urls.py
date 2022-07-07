from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('',views.all_products, name='all_products'),
    path('<slug:slug>',views.product_details, name='product_details'),
    path('search/<slug:category_slug>/',views.category_list, name='category_list'),
    
]
