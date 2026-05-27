from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView,FormView,CreateView
from student.forms import *
from django.urls import reverse_lazy

# Create your views here.

# class SigninView(View):
#     def get(self,request):
#         return render(request,'signin.html')
    
class SigninView(FormView):
    template_name='signin.html'
    form_class=SignInForm


# class SignupView(View):
#     def get(self,request):
#         return render(request,'signup.html')

class SignupView(CreateView):
    template_name='signup.html'
    form_class=StudentSignUpForm
    success_url=reverse_lazy('signin')