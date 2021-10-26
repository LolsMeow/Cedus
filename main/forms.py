from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *


# Create your forms here.

class register(UserCreationForm):
    first_name = forms.CharField(label='', max_length=30, required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label='', max_length=30, required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(label='', required=True,
                            widget=forms.TextInput(attrs={'placeholder': 'Email Address'}))
    password1 = forms.CharField(label='', required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label='', required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', "email", "password1", "password2")
        help_text = {
            'password1': None,
            'password2': None
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                ("This email address is already in use. Please supply a different email address."))
        return email

    def save(self, commit=True):
        user = super(register, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = user.email
        if commit:
            user.save()
        return user

class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ()


class DateInput(forms.DateInput):
    input_type = 'date'


class infoReg(ModelForm):
    birth_date = forms.DateField(label="", widget=DateInput())
    class Meta:
        model = Patient
        fields = ('birth_date', 'phone_number', 'street_address', 'apt', 'city', 'state', 'zip_code')

class userInfo(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                ("This email address is already in use. Please supply a different email address."))
        return email

    def save(self, commit=True):
        user = super(userInfo, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = user.email
        if commit:
            user.save()
        return user


class updateInfo(ModelForm):
    birth_date = forms.DateField(label="", widget=DateInput())
    class Meta:
        model = Patient
        fields = ['birth_date', 'phone_number', 'street_address', 'apt', 'city', 'state', 'zip_code']
        exclude = ['user', 'provider_name', 'plan_name', 'rx_bin', 'id_number', 'rx_pcn', 'rx_group']
