from django.contrib import admin
from instructor.models import *
from django.contrib.admin import ModelAdmin,TabularInline

# Register your models here.
admin.site.register(User)
admin.site.register(category)

class CourseModelAdmin(ModelAdmin):
    exclude=('instructor',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.instructor=request.user
        return super().save_model(request, obj, form, change)
admin.site.register(Course,CourseModelAdmin)

class LessonInline(TabularInline):
    model=Lesson
    extra=1
    exclude=("order_number",)


class ModuleModelAdmin(ModelAdmin):
    exclude=('order_number',)
    inlines=[LessonInline]
admin.site.register(Module,ModuleModelAdmin)


class profileModelAdmin(ModelAdmin):
    exclude=('instructor',)


    def get_queryset(self, request):
        qs=super().get_queryset(request)
        return qs.filter(instructor=request.user) 
    
    def has_add_permission(self, request):
        return False
    

admin.site.register(InstructorProfile,profileModelAdmin)

class LessonModelAdmin(ModelAdmin):
    exclude=('order_number',)

# admin.site.register(Lesson,LessonModelAdmin)
