from base64 import urlsafe_b64decode
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.urls import reverse
from .forms import PasswordResetForm, RegistrationForm, UserAddressForm
from .tokens import account_activation_token
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import login ,user_logged_in

from .models import ShippingAddress, UserBase
# Create your views here.
@login_required
def dashboerd(request):
    return render(request, 'account/user/dashboard.html')


def account_register(request):
    

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            # setup email
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('account/registration/account_activation.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            #user.send_mail(subject=subject, message= message)
            #return PROMPT("your account has been registered and activation link is send")

    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})

def account_activation(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except:
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')

def password_reset(request):
    if request.method == 'POST':
        passwordForm = PasswordResetForm(request.POST)
        if passwordForm.is_valid():
            user = passwordForm.save(commit=False)
            user.email = passwordForm.cleaned_data['email']
            user.set_password(passwordForm.cleaned_data['password'])
            user.is_active = False
            user.save()
    return render(request, 'account/password_reset.html')

def view_address(request):
    addresses = ShippingAddress.objects.filter(user=request.user)
    return render(request, 'account/addresses.html', {"addresses": addresses})

def add_address(request):
    print(request.POST.keys())
    print(request.user.id)
    if request.method == 'POST':
        address_form = UserAddressForm(request.POST)
        
        if address_form.is_valid():
            print(request.user.id)
            address_form = address_form.save(commit=False)
            address_form.user = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
            address_form = UserAddressForm()
    return render(request, 'account/edit_address.html', {"form": address_form})

def delete_address(request,id):

    ShippingAddress.objects.filter(pk=id, user=request.user).delete()
    
    return redirect("account:addresses")

def edit_address(request,id):
    
    if request.method == 'POST':
        address = ShippingAddress.objects.filter(pk=id, user=request.user)
        address_form = UserAddressForm(instance = address, data = request.POST)
        print(address)
        print(address_form)
        if address_form.is_valid():
            
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address = ShippingAddress.objects.filter(pk=id, user=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, 'account/edit_address.html', {"form": address_form})

def default_address(request,id):
    ShippingAddress.objects.filter(user=request.user, default=True).update(default=False)
    ShippingAddress.objects.filter(pk=id).update(default=True)
    return redirect("account:addresses")





    


