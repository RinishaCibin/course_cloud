from django import forms 
from instructor.models import User
from django.contrib.auth.forms import UserCreationForm

class StudentSignUpForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]

class SignInForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"w-full px-1 py-1 border rounded bg-white"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"w-full px-1 py-1 border rounded bg-white"}))