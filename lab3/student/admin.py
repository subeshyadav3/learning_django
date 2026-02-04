from django.contrib import admin
from .models import StudentModel,SemesterMarks
# Register your models here.
admin.site.register(StudentModel)
admin.site.register(SemesterMarks)


from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active')