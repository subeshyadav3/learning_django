from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from .models import StudentModel, SemesterMarks
from .form import StudentForm, SemesterMarksForm

# Create your views here.
def student_list(request):
    if request.method=='GET':
        students=StudentModel.objects.all()
        context={'students':students}
        return render(request,'student_list.html',context)

    
def student_create(request):
    if request.method=='POST':
        form=StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/student')
    
    return render(request,'student_create.html',{'form':StudentForm()} )

def student_create_marks(request):
    if request.method=='POST':
        form=SemesterMarksForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/student')
    
    return render(request,'student_create_marks.html',{'form':SemesterMarksForm()})


def home(requst):
    return HttpResponse("Welcome to the Student Home Page")


from django.shortcuts import render, get_object_or_404

def student_details(request, pk):
    student = get_object_or_404(StudentModel, pk=pk)
    marks = student.marks.all()
    
    context = {
        'student': student,
        'marks': marks
    }
    return render(request, 'student_details.html', context)


from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login
from .form import LoginForm, RegisterForm

def register_view(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form=RegisterForm()
    return render(request,'register.html',{'form':form})

def login_view(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            user=form.cleaned_data.get('user')
            login(request,user)
            return redirect('/dashboard')
    else:
        form=LoginForm()
    return render(request,'login.html',{'form':form})

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    request.session['last_login']=str(request.user.last_login)
    response=render(request,'dashboard.html')

    response.set_cookie(key='name',value='subesh', httponly=True, secure=False)
    print("User Role:", request.user.last_login)
    return response


from django.conf import settings
from .models import User

@login_required
def admin_panel(request):
    if request.user.role != 'admin':
        return redirect('dashboard')  

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        role = request.POST.get('role')
        try:
            user = User.objects.get(id=user_id)
            user.role = role
            user.save()
        except User.DoesNotExist:
            pass
        return redirect('admin_panel')

    users = User.objects.all()
    return render(request, 'admin_panel.html', {'users': users})
