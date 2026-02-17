from django.urls import path
from .views import student_list, student_details, student_create, student_create_marks

urlpatterns=[
    path('', student_list, name='student-home'),
    path('details/<int:pk>/', student_details, name='details'),
    path('create/', student_create, name='create'),
    path('create/marks/', student_create_marks, name='marks'),
]