from django.contrib import admin
from .models import Category, Product

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepoppulated_fields = {'slug':('name')}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','authur','slug','price','in_stock','created','updated']
    list_filter = ['in_stock','is_active']
    list_editable = ['price','in_stock']
    prepoppulated_field = {'slug':('name')}