from django.urls import path,include
from .views import Student,getSingleStudent

urlpatterns = [
    path('student/', Student, name='student_list'),
    path('student/<int:pk>/', getSingleStudent, name='single_student'),
    path('employee/', include('employee.urls')),
]
