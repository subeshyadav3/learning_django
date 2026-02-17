from django.urls import path
from .views import student_list, student_create, student_add

# urlpatterns = [
#     path('', student_list, name='student_list'),
#     path('add/', student_create, name='student_create'),
# ]


urlpatterns = [
    path('', student_list.as_view(), name='student_list'),
    path('add/', student_create.as_view(), name='student_create'),
    path('adds/', student_add, name='student_add'),

]

