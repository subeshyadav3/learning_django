from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def register(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect("task_list")

    else:
        form = RegisterForm()

    return render(request,"tasks/register.html",{"form":form})


def user_login(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request,username=username,password=password)

        if user:
            login(request,user)
            return redirect("task_list")

    return render(request,"tasks/login.html")


@login_required
def task_list(request):

    tasks = Task.objects.filter(user=request.user)

    return render(request,"tasks/task_list.html",{"tasks":tasks})


@login_required
def add_task(request):

    form = TaskForm(request.POST or None)

    if form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        return redirect("task_list")

    return render(request,"tasks/add_task.html",{"form":form})


@login_required
def delete_task(request,id):

    task = Task.objects.get(id=id)
    task.delete()

    return redirect("task_list")


def user_logout(request):

    logout(request)
    return redirect("login")