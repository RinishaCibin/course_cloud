from instructor.views import InstructorSignupView
from django.urls import path

urlpatterns=[
    path('insignup',InstructorSignupView.as_view(),name="insreg")
]