from student.models import Cart,WishList,Order

def cart_count(request):
    if request.user.is_authenticated:
        cnt=Cart.objects.filter(student_object=request.user).count()
        return {"cart_count":cnt}
    else:
        return {"cart_count":0}

def wish_count(request):
    if request.user.is_authenticated:
        cnt=WishList.objects.filter(student_object=request.user).count()
        return {"wish_count":cnt}
    else:
        return {"wish_count":0}

def course_count(request):
    if request.user.is_authenticated:
        qs=Order.objects.filter(is_paid=True,student_object=request.user)
        course_count=0
        for i in qs:
            course_count+=i.course_object.count()
        return {"course_count":course_count}
    else:
        return {"course_count":0}