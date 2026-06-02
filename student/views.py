from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import TemplateView,FormView,CreateView,ListView,DetailView
from student.forms import *
from django.urls import reverse_lazy,reverse
from django.contrib.auth import authenticate,login
from django.contrib import messages
from instructor.models import Course
from student.models import*

# Create your views here.

# class SigninView(View):
#     def get(self,request):
#         return render(request,'signin.html')
    
class SigninView(FormView):
    template_name='signin.html'
    form_class=SignInForm

    def post(self,request):
        form_data=SignInForm(data=request.POST)
        if form_data.is_valid():
            uname=form_data.cleaned_data.get('username')
            pswd=form_data.cleaned_data.get('password')
            user=authenticate(request,username=uname,password=pswd)
        if user:
            login(request,user)
            if user.role=="Student":
                return redirect('shome')
            elif user.role=="Instructor":
                return redirect(reverse('admin:index'))
            else:
                messages.error(request,"Invalid Username/Password")
                return redirect('signin')
        return render(request,"signin.html",{"form":form_data})



# class SignupView(View):
#     def get(self,request):
#         return render(request,'signup.html')

class SignupView(CreateView):
    template_name='signup.html'
    form_class=StudentSignUpForm
    success_url=reverse_lazy('signin')

class StudentHomeView(ListView):
    template_name='studentHome.html'
    queryset=Course.objects.all()
    context_object_name="courses"

class CourseDetailsView(DetailView):
    template_name="courseDetails.html"
    queryset=Course.objects.all()
    pk_url_kwarg="cid"
    context_object_name="course"

class AddtoCartView(View):
    def get(self,request,**kwargs):
        cid=kwargs.get('cid')
        course=Course.objects.get(id=cid)
        student=request.user
        (object,created)=Cart.objects.get_or_create(course_object=course,student_object=student)
        print(object,created)
        if created:
            return redirect('shome')
        else:
            messages.warning(request,"Course Already added to cart!!")
            return redirect('shome')

