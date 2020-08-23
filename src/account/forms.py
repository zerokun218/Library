from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

class StudentSignUpForm(UserCreationForm):
    dob = forms.DateField(label='Date of birth:', input_formats=['%Y/%m/%d','%Y/%m','%d/%m/%Y','%d-%m-%Y', '%m/%Y', '%m-%Y'])
    address = forms.CharField(required=False)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'dob', 'email', 'address', 'password1', 'password2']
        labels = {
            'dob': 'Date of birth',
            'username': 'Account'
        }
