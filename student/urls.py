from django.urls import path
from student.views import *

urlpatterns = [
    path('signup',SignupView.as_view(),name='signup'),
    path('student-home',StudentHomeView.as_view(),name='shome'),
    path('course-details/<int:cid>',CourseDetailsView.as_view(),name='course_details'),
    path('addtocart/<int:cid>',AddToCartView.as_view(),name="addtocart"),
    path('cartlist',CartListView.as_view(),name='cartlist'),
    path('remcart/<int:cid>',RemoveCartView.as_view(),name='remcart'),
    path('addtowish/<int:cid>',AddToWishlistView.as_view(),name='addtowish'),
    path('wishlist',WishlistShowView.as_view(),name='wishlist'),
    path('remwish/<int:cid>',RemoveWishlistView.as_view(),name='remwish'),
    path('checkout',PlaceOrderView.as_view(),name='placeorder'),
    path('paymentveify',PayementVerify.as_view(),name='paymentverify'),
    path('mycourses',MyCoursesView.as_view(),name='mycourses')

]