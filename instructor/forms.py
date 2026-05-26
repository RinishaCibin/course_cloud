from django import forms
from instructor.models import User
from django.contrib.auth.forms import UserCreationForm

class InstructorForm(UserCreationForm):
    class Meta:
        model=User
        fields=["first_name","last_name","username","email","password1","password2"]