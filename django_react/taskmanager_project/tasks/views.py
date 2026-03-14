from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Task
import json

@csrf_exempt
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return JsonResponse({"error": "Username and password required"}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)
        user = User.objects.create_user(username=username, password=password)
        return JsonResponse({"message": "User registered successfully", "user_id": user.id})
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def user_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({"message": "Login successful", "user_id": user.id})
        return JsonResponse({"error": "Invalid credentials"}, status=401)
    return JsonResponse({"error": "Invalid request method"}, status=405)


def user_logout(request):
    logout(request)
    return JsonResponse({"message": "Logged out successfully"})



@csrf_exempt
def task_list(request):
    if request.method == "GET":
        tasks = Task.objects.all().values("id", "title", "description", "completed")
        return JsonResponse(list(tasks), safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def add_task(request):
    if request.method == "POST":
        data = json.loads(request.body)
        title = data.get("title")
        description = data.get("description", "")
        if not title:
            return JsonResponse({"error": "Title is required"}, status=400)
        task = Task.objects.create(title=title, description=description, completed=False)
        return JsonResponse({"message": "Task created", "task_id": task.id})
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def edit_task(request, id):
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)
        task.title = data.get("title", task.title)
        task.description = data.get("description", task.description)
        if "completed" in data:
            task.completed = data.get("completed")
        task.save()
        return JsonResponse({"message": "Task updated"})
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def delete_task(request, id):
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)

    if request.method == "DELETE":
        task.delete()
        return JsonResponse({"message": "Task deleted"})
    return JsonResponse({"error": "Invalid request method"}, status=405)