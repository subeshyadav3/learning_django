from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    credits = models.IntegerField(default=3)
    department = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(unique=True, db_index=True, null=True, blank=True)
    courses = models.ManyToManyField(Course, through='Enrollment')
    active = models.BooleanField(default=True)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    grade = models.CharField(max_length=2, null=True, blank=True)  # e.g., A, B, C
    semester = models.CharField(max_length=10, null=True, blank=True)  # e.g., Fall 2025

    class Meta:
        unique_together = ('student', 'course', 'semester')

    def __str__(self):
        return f"{self.student.name} enrolled in {self.course.code}"
