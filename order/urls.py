from django.urls import path
from django.contrib import admin

from . import views

app_name = 'order'
urlpatterns = [
    path('add/', views.view_order, name='order_summary'),
    path('', views.orders, name='orders')
    ]