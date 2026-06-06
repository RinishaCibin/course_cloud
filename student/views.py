from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import TemplateView,FormView,CreateView,ListView,DetailView
from student.forms import *
from django.urls import reverse_lazy , reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from instructor.models import Course,Module,Lesson
from student.models import *
from django.db.models import Count
import razorpay
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from decouple import config



RAZOR_PAY_KEY=config('RAZOR_PAY_KEY')
RAZOR_PAY_SECRET_KEY=('RAZOR_PAY_SECRET_KEY')

# signin required

def signin_required(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.warning(request,"please login first")
            return redirect('signin')
    return inner

# Create your views here.

# class SigninView(View):
#     def get(self,request):
#         return render(request,'signin.html')
    
class SigninView(FormView):
    template_name='signin.html'
    form_class=SignInForm

    def post(self, request):
        form_data=SignInForm(data=request.POST)
        if form_data.is_valid():
            uname=form_data.cleaned_data.get('username')
            pswd=form_data.cleaned_data.get('password')
            user=authenticate(request,username=uname,password=pswd)
            if user:
                login(request,user)
                if user.role=='Student':
                    return redirect('shome')
                elif user.role=='Instructor':
                    return redirect(reverse('admin:index'))
                else:
                    messages.error(request,"Invalid Username or Password")
                    return redirect('signin')
            return render(request,"signin.html",{"form":form_data})



# class SignupView(View):
#     def get(self,request):
#         return render(request,'signup.html')

class SignupView(CreateView):
    template_name='signup.html'
    form_class=StudentSignUpForm
    success_url=reverse_lazy('signin')

@method_decorator([csrf_exempt,never_cache],name="dispatch")
class SignOutView(View):
    def get(self,request):
        logout(request)
        return redirect('signin')
    
@method_decorator([csrf_exempt,never_cache],name="dispatch")
class StudentHomeView(ListView):
    template_name='studenthome.html'
    queryset=Course.objects.all()
    context_object_name="courses"
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        purchased_courses=Order.objects.filter(student_object=self.request.user,is_paid=True).values_list("course_object",flat=True)
        context["purchased_courses"]=purchased_courses
        return context
    
@method_decorator([csrf_exempt,never_cache],name="dispatch")
class CourseDetailsView(DetailView):
    template_name='coursedetails.html'
    queryset=Course.objects.all()
    pk_url_kwarg='cid'
    context_object_name='course'

@method_decorator([csrf_exempt,never_cache],name="dispatch")
class AddToCartView(View):
    def get(self,request,**kwargs):
        cid=kwargs.get('cid')
        course=Course.objects.get(id=cid)
        student=request.user
        (object,created)=Cart.objects.get_or_create(course_object=course,student_object=student)
        if created:
            return redirect('shome')
        else:
            messages.warning(request,"Course Already Added To Cart !!!")
            return redirect('shome')
        
@method_decorator([csrf_exempt,never_cache],name="dispatch")  
class CartListView(View):
    def get(self,request):
        cart_list=Cart.objects.filter(student_object=request.user)
        cart_count=cart_list.count()
        cart_total=0
        for i in cart_list:
            cart_total+=i.course_object.price
        return render(request,"cartlist.html",{"data":cart_list,"count":cart_count,"cart_total":cart_total})
    
@method_decorator([csrf_exempt,never_cache],name="dispatch")  
class RemoveCartView(View):
    def get(self,request,**kwargs):
        cid=kwargs.get('cid')
        Cart.objects.get(id=cid).delete()
        return redirect('cartlist')
    
@method_decorator([csrf_exempt,never_cache],name="dispatch")
class AddToWishlistView(View):
    def get(self,request,**kwargs):
        cid=kwargs.get('cid')
        c=Course.objects.get(id=cid)
        student=request.user
        (object,created)=WishList.objects.get_or_create(course_object=c,student_object=student)
        if created:
            return redirect('shome')
        else:
              messages.warning(request,"Course Already Added To WishList !!!")
              return redirect('shome')
        
@method_decorator([csrf_exempt,never_cache],name="dispatch")
class WishlistShowView(View):
    def get(self,request):
        wish_no=WishList.objects.filter(student_object=request.user)
        count=wish_no.count()
        return render(request,"wishlist.html",{"data":wish_no,"count":count})
    
@method_decorator([csrf_exempt,never_cache],name="dispatch")
class RemoveWishlistView(View):
    def get(self,request,**kwargs):
        cid=kwargs.get('cid')
        WishList.objects.get(id=cid).delete()
        return redirect('wishlist')
    
@method_decorator([csrf_exempt,never_cache],name="dispatch")
class PlaceOrderView(View):
    def get(self,request):
        student=request.user
        qs=Cart.objects.filter(student_object=student)
        cart_total=0
        for i in qs:
            cart_total+=i.course_object.price
        order=Order.objects.create(student_object=student,total=cart_total)
        for i in qs:
            order.course_object.add(i.course_object)
        qs.delete()
        if cart_total>0:
            client=razorpay.Client(auth=(RAZOR_PAY_KEY,RAZOR_PAY_SECRET_KEY))
            data={"amount":int(cart_total),"currency":"INR","receipt":"order_rcptid_11"}
            payment=client.order.create(data=data)
            print("payment")
            order.razr_pay_order_id=payment.get('id')
            order.save()
            context={
                "razr_pay_key":RAZOR_PAY_KEY,
                "amount":int(cart_total),
                "razr_pay_order_id":payment.get('id')
            }
            return render(request,"payment.html",{"data":context})
        elif cart_total==0:
            order.is_paid=True
            order.save()
            return redirect('shome')
        return redirect('shome')
    
@method_decorator([csrf_exempt],name="dispatch")    
class PaymentVerify(View):
    def post(self,request):
        print(request.POST)
        client=razorpay.Client(auth=(RAZOR_PAY_KEY,RAZOR_PAY_SECRET_KEY))
        try:
            client.utility.verify_payment_signature(request.POST)
            rzr_pay_order_id=request.POST.get('razorpay_order_id')
            order=Order.objects.get(razr_pay_order_id=rzr_pay_order_id)
            order.is_paid=True
            order.save()
        except Exception as e:
            print(e)
            print("Failed")
        return redirect('shome')
class MyCourseView(View):
    def get(self,request):
        order_qs=Order.objects.filter(is_paid=True,student_object=request.user)
        return render(request,"mycourses.html",{"data":order_qs})
    
@method_decorator([csrf_exempt,never_cache],name="dispatch")
class ViewLessonView(View):
    def get(self,request,**kwargs):
        cid=kwargs.get('cid')
        course=Course.objects.get(id=cid)
        module=Module.objects.filter(course=course).first()
        lesson=Lesson.objects.filter(module=module).first() if 'lesson' not in request.GET else Lesson.objects.get(id=request.GET.get('lesson'))
        return render(request,'viewlessons.html',{"course":course,"lesson":lesson})
    
