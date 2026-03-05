from django.urls import path
from . import views

urlpatterns = [

    path("",views.task_list,name="task_list"),
    path("add/",views.add_task,name="add_task"),
    path("delete/<int:id>/",views.delete_task,name="delete_task"),

    path("login/",views.user_login,name="login"),
    path("register/",views.register,name="register"),
    path("logout/",views.user_logout,name="logout"),
]