from django.shortcuts import render,redirect
from .models import GeeksModel
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView
from .forms import InputForm

# def GeekViews(request):
#     context ={}
#     context['dataset']=GeeksModel.objects.all()
#     return render(request, 'list_view.html', context)

class GeekViews(ListView):

    model=GeeksModel
    template_name='list_view.html'
    context_object_name='dataset'

def home(request):
    return HttpResponse("Welcome to Home Page")

# def my_view(request):
#     if request.method=='POST':
#         title=request.POST.get('title')
#         description=request.POST.get('description')

#         geek=GeeksModel(title=title,description=description)
#         geek.save()
#         return redirect('/accounts/')

#     return render(request,'form.html')
        
def my_view(request):
    if request.method=='POST':
        form=InputForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data['title']
            description=form.cleaned_data['description']
            geek=GeeksModel(title=title,description=description)
            geek.save()
            return redirect('/accounts/')

    return render(request,'form.html',{'form':InputForm()})


