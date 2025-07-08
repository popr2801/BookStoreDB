from django import forms
from .models import User

class UserForm(forms.ModelForm):
    firstname = forms.CharField(label="First Name", max_length=100)
    lastname = forms.CharField(label="Last Name", max_length=100)
    email = forms.EmailField(label="Email Address")
    phone = forms.CharField(label="Phone Number", max_length=20)
    password = forms.CharField(label="Password", max_length=256, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'email', 'phone']

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(label="Password",max_length=100,widget = forms.PasswordInput)

