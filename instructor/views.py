from django.shortcuts import render,redirect
from django.views import View
from instructor.forms import InstructorForm
from django.contrib import messages


# Create your views here.

class InstructorSignupView(View):
    def get(self,request):
        form=InstructorForm()
        return render(request,"instructor_signup.html",{"form":form})
    
    def post(self,request):
        form_data=InstructorForm(data=request.POST)
        if form_data.is_valid():
            instructor=form_data.save(commit=False)
            instructor.is_superuser=True
            instructor.is_staff=True
            instructor.role="Instructor"
            instructor.save()
            messages.success(request,"Instructor Registered")
            return redirect('insreg')
        return render(request," instructor_signup.html",{"form":form_data})
        


