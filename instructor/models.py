from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Max

# Create your models here.
class User(AbstractUser):
    role_options=[
        ("Student","Student"),
        ("Instructor","Instructor")
        
    ]
    role=models.CharField(max_length=50,choices=role_options)

class InstructorProfile(models.Model):
    expertise=models.CharField(max_length=100,null=True)
    insructor_picture=models.ImageField(upload_to="instructor_picture",default="Instructor_profile_logo.png")
    about=models.CharField(max_length=500,null=True)
    instructor=models.OneToOneField(User,on_delete=models.CASCADE,related_name="instructor_profile")

    def __str__(self):
        return self.instructor.username
    
# signals reciever to create profile instance while a user created
@receiver(post_save,sender=User)
def create_instructor_profile(sender,instance,created,**kwargs):
    if created and instance.role=="Instructor":
        InstructorProfile.objects.create(instructor=instance)



class category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Course(models.Model):
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    price=models.DecimalField(max_digits=7,decimal_places=2,default=0)
    instructor=models.ForeignKey(User,on_delete=models.CASCADE,related_name="course")
    is_free=models.BooleanField(default=False)
    course_picture=models.ImageField(upload_to="Course_Picture")
    thumbnail=models.TextField()
    category=models.ManyToManyField(category)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Module(models.Model):
    title=models.CharField(max_length=100)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="modules")
    order_number=models.PositiveBigIntegerField()

    def __str__(self):
        return f"{self.order_number}.{self.title}"
    
    def save(self,*args,**kwargs):
        max_order=Module.objects.filter(course=self.course).aggregate(max=Max("order_number")).get('max') or 0
        self.order_number=max_order+1
        super().save(*args,**kwargs)
    class Meta:
        ordering=["order_number"]
    
class Lesson(models.Model):
    title=models.CharField(max_length=100)
    module=models.ForeignKey(Module,on_delete=models.CASCADE,related_name="lessons")
    video=models.TextField()
    order_number=models.PositiveBigIntegerField()

    def __str__(self):
        return f"{self.order_number}.{self.title}"
    
    def save(self,*args,**kwargs):
        max_order=Lesson.objects.filter(module=self.module).aggregate(max=Max("order_number")).get('max') or 0
        self.order_number=max_order+1
        super().save(*args,**kwargs)
    class Meta:
        ordering=["order_number"]


