from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import TaskForm, RegisterForm
from .models import Task
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("task_list")
        else:
            messages.error(request, "Invalid data!")
    else:
        form = RegisterForm()
    return render(request, "tasks/register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("task_list")
        else:
            messages.error(request, "Invalid credentials")
    return render(request, "tasks/login.html")

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect("login")

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, "tasks/task_list.html", {"tasks": tasks})

@login_required
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, "Task added successfully")
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "tasks/add_task.html", {"form": form})

@login_required
def edit_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully")
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/add_task.html", {"form": form})

@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.delete()
    messages.success(request, "Task deleted successfully")
    return redirect("task_list")