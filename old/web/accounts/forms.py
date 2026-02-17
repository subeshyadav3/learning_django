from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import GeeksModel

class RegisterForm(forms.ModelForm):
    username=forms.CharField()
    password=forms.CharField()
    confirm_password=forms.CharField()

    class Meta:
        model = User
        fields = ['username','password']

class LoginForm(forms.ModelForm):
    username=forms.CharField()
    password=forms.CharField()

    class Meta:
        model = User
        fields = ['username','password']

class InputForm(forms.Form):
    title=forms.CharField(max_length=200,help_text="Enter Title",required=True,error_messages={'required':'Title is required'})
    description=forms.CharField(widget=forms.Textarea,help_text="Enter Description")

class GeeksForm(forms.ModelForm):
    class Meta:
        model = GeeksModel
        fields = ['title','description']