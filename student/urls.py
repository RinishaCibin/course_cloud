from django.urls import path
from student.views import *

urlpatterns = [
    path('signup',SignupView.as_view(),name='signup'),
    path('student-home',StudentHomeView.as_view(),name='shome'),
    path('course-details/<int:cid>',CourseDetailsView.as_view(),name='course_details')

]