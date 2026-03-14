from django.urls import path
from . import views

urlpatterns = [

    # Authentication
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

    # Task API 
    path("", views.task_list, name="task_list"),         
    path("create/", views.add_task, name="add_task"),     
    path("<int:id>/", views.edit_task, name="edit_task"),
    path("delete/<int:id>/", views.delete_task, name="delete_task"), 
]