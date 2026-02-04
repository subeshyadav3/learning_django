from django.contrib import admin

# Register your models here.

from .models import StudentModel
admin.site.register(StudentModel)
