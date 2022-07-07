from django.urls import path
from django.contrib import admin

from . import views

app_name = 'payment'
urlpatterns = [
    path('', views.payment_summary, name='payment_summary'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('admin/', admin.site.urls),
    

]