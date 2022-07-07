
from django import  forms
from django.contrib.auth.forms import AuthenticationForm,PasswordResetForm
from .models import ShippingAddress, UserBase

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs = {'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'login-username'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs = {'class': 'form-control', 'placeholder': 'Password', 'id': 'login-pwd'}
    ))


class RegistrationForm(forms.ModelForm):
    
    user_name = forms.CharField(label= 'Enter Username',min_length=5, max_length= 50, help_text='Required')
    email = forms.EmailField( max_length=20, help_text='Required', error_messages={'required':'Email is mandatory'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('user_name','email',)
    
    def clean_user_name(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return user_name
    
    def clean_confirm_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['confirm_password']:
            raise forms.ValidationError("Password do not match")
        return cd['confirm_password']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['confirm_password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Confirm Password'})

    

class UserAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ["first_name", "phone_number", "address", "postcode", "city", "state", "country"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control mb-3' , 'placeholder': 'Name'})
        self.fields['phone_number'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Phone'})
        self.fields['address'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Address'})
        self.fields['postcode'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Pincode'})
        self.fields['city'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'City'})
        self.fields['state'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'State'})
        self.fields['country'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Country'})

        


    
    
    
    