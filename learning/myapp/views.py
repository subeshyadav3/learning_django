from django.shortcuts import render,redirect
from .models import Student
from .forms import StudentForm
from django.views import View
from django.http import HttpResponse
# def home(request):
#     return render(request,'home.html')



# def student_list(request):
#     students=Student.objects.all()
#     return render(request,'student_list.html',{'students':students})



# def student_create(request):
#     if request.method=='POST':
#         form=StudentForm(request.POST)
#         if(form.is_valid()):
#             form.save()
#             return redirect('student_list')
#     else:
#         form=StudentForm()

#     return render(request,'student_form.html',{'form':form})


class home(View):
    def get(self,requset):
        return render(requset,'home.html')


class student_list(View):
    def get(self,request):
        students=Student.objects.all()
        return render(request,'student_list.html',{'students':students})
    
class student_create(View):
    def get(self,request):
        form=StudentForm()
        return render(request,'student_form.html',{'form':form})
    
    def post(self,request):
        form=StudentForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('student_list')
        return render(request,'student_form.html',{'form':form})




def student_detail(request, id,role):
    return HttpResponse(f"Student ID: {id} Role: {role}")



def student_add(request):
    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        email = request.POST.get("email")

 
        if name and age and gender:
            Student.objects.create(
                name=name,
                age=age,
                gender=gender,
                email=email
            )
            return redirect("student_list")

    return render(request, "add_student.html")