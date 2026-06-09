from django.shortcuts import render , redirect
from django.views import View
from instructor.forms import InstructorForm
from django.contrib import messages

# Create your views here.
class InstructorSignUpView(View):
    def get(self,request):
        form=InstructorForm()
        return render(request,"instructor_signup.html",{"form":form})
    def post(self,request,**kwargs):
        form_data=InstructorForm(data=request.POST)
        if form_data.is_valid():
            inst=form_data.save(commit=False)
            inst.is_superuser=True
            inst.is_staff=True
            inst.role="Instructor"
            inst.save()
            messages.success(request,"Instructor Registerd!")
            return redirect('insreg')
        return render(request,"instructor_signup.html",{"form":form_data})
