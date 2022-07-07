
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import UserLoginForm

app_name = 'account'

urlpatterns = [
    path('register/',views.account_register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='account/registration/login.html',form_class=UserLoginForm),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='/account/login/'),name='logout'),
    
    path('activate/<slug:uidb64>/<slug:token>)/',views.account_activation,name='activate'),
    path('password_reset/',views.password_reset,name='password_reset'),
    path('dashboerd/',views.dashboerd,name='dashboerd'),
    path('addresses/',views.view_address,name='addresses'),
    path('addresses/add/',views.add_address,name='add_address'),
    path('addresses/<slug:id>',views.delete_address,name='delete_address'),
    path('addresses/edit/<slug:id>',views.edit_address,name='edit_address'),
    path('addresses/default/<slug:id>',views.default_address,name='default_address'),
]
