import re
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import user_detail,Plan, paymentmethod_detail

class RegistrationForm(forms.Form):
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'placeholder',
            'placeholder': 'Enter your full name'
        })
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'placeholder',
            'placeholder': 'Enter your email'
        })
    )

    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'placeholder',
            'placeholder': 'Enter your phone number'
        })
    )

    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'placeholder',
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'placeholder',
            'placeholder': 'Enter your password'
        })
    )


def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')

        # Check if the full name contains at least two words
        words = full_name.split()
        if len(words) < 2:
            raise ValidationError('Please enter your full name.')

        # Check if the full name contains only letters (no numbers or special characters)
        if not re.match(r'^[a-zA-Z\s]+$', full_name):
            raise ValidationError('Full name should contain only letters.')

        return full_name

def clean_email(self):
    email = self.cleaned_data.get('email')

        # Check if the email already exists in the User model
    if User.objects.filter(email=email).exists():
        raise ValidationError('This email address is already in use.')

        # Validate email format using regex
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        raise ValidationError('Enter a valid email address.')

    return email
    
def clean_phone(self):
    phone = self.cleaned_data.get('phone')

    # Validate phone number using a regular expression
    # This is a basic example and might need adjustments based on phone number format requirements
    phone_regex = r'^\+?1?\d{9,15}$'  # Example regex for numbers between 9 to 15 digits
    if not re.match(phone_regex, phone):
        raise ValidationError('Enter a valid phone number.')

    return phone

def clean_username(self):
    username = self.cleaned_data.get('username')

        # Check if the username contains whitespace
    if ' ' in username:
            raise ValidationError('Username cannot contain whitespace.')

    return username

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'placeholder',
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'placeholder',
            'placeholder': 'Enter your password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                self.add_error("password", "Invalid username or password")
        return cleaned_data


class PaymentMethodForm(forms.ModelForm):
    
    cardtype = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'placeholder',
            'placeholder': 'Enter your cardtype'
        })
    )

    expirymonth = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'placeholder',
            'placeholder': 'Enter your expirymonth'
        })
    )
    
    expiryyear = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'placeholder',
            'placeholder': 'Enter your expiryyear'
        })
    )

    CVV = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'placeholder',
            'placeholder': 'Enter your CVV'
        })
    )

    cardnumber = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'placeholder',
            'placeholder': 'Enter your cardnumber'
        })
    )

    cardholdername = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'placeholder',
            'placeholder': 'Enter your cardholdername'
        })
    )



    def clean_card_number(self):
        cardnumber = self.cleaned_data['cardnumber']
        if not re.match(r'^\d{16}$', cardnumber):
            raise forms.ValidationError("Card number must contain exactly 16 digits.")
        return cardnumber

    def clean_expiry_month(self):
        expiration_month = self.cleaned_data['expiration_month']
        if not expiration_month.isdigit():
            raise forms.ValidationError("Expiration month must contain only digits.")
        return expiration_month

    def clean_expiry_year(self):
        expiryyear = self.cleaned_data['expiryyear']
        if not expiryyear.isdigit():
            raise forms.ValidationError("Expiration year must contain only digits.")
        return expiryyear

    def clean_CVV(self):
        CVV = self.cleaned_data['CVV']
        if not CVV.isdigit():
            raise forms.ValidationError("CVV must contain only digits.")
        return CVV

    def save(self, user=None, commit=True):
        instance = super().save(commit=False)
        if user:
            instance.user = user
        if commit:
            instance.save()
        return instance

    class Meta:
        model = paymentmethod_detail
        fields = ['cardtype', 'cardholdername', 'cardnumber', 'expirymonth', 'expiryyear', 'CVV']


class PhonePlanForm(forms.ModelForm):

    plan = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'placeholder',
            'placeholder': 'Enter your plan:'
        })
    )

    amount = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'placeholder',
            'placeholder': 'Enter your amount:'
        })
    )

    class Meta:
        model = Plan
        fields = ['plan', 'amount']  