from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'birth_date', 'password1', 'password2']
