from django.urls import path
from instructor.views import InstructorSignUpView

urlpatterns=[
    path("instructorsignup",InstructorSignUpView.as_view(),name='insreg'),
]