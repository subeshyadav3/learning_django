from django.contrib import admin
# from .models import GeeksModel


from .models import Student

@admin.register(Student)    

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'age','email','gpa')
    search_fields = ('name','email')
    list_filter = ('age','gpa')
