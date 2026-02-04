from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class StudentModel(models.Model):
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    email=models.EmailField()
    def __str__(self):
        return self.name

class SemesterMarks(models.Model):
    student=models.ForeignKey(StudentModel, on_delete=models.CASCADE, related_name='marks')
    semester=models.IntegerField()
    marks=models.FloatField()

    def __str__(self):
        return f"Semester {self.semester} - {self.marks}"

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('user', 'User'),
    )

    role=models.CharField(max_length=20,choices=ROLE_CHOICES,default='user')

    def is_admin(self):
        return self.role=='admin'

    def is_staff_user(self):
        return self.role=='staff'
