from django.forms import ModelForm
from .models import StudentModel, SemesterMarks,User
from django.contrib.auth import authenticate
from django import forms
from .models import User

class StudentForm(ModelForm):
    class Meta:
        model = StudentModel
        fields = ['name', 'age', 'email']

class SemesterMarksForm(ModelForm):
    class Meta:
        model = SemesterMarks
        fields = ['student', 'semester', 'marks']


class RegisterForm(ModelForm):
    password1=forms.CharField(widget=forms.PasswordInput)
    password2=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=['username','email','role']

    def clean(self):
        cleaned_data=super().clean()
        password1=cleaned_data.get('password1')
        password2=cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    
    def save(self):#hash password before saving
        user=super().save(commit=False)
        password=self.cleaned_data.get('password1')
        user.set_password(password)
        user.save()
        return user

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data=super().clean() ## calls ModelForm clean method
        username=cleaned_data.get('username')
        password=cleaned_data.get('password')

        user=authenticate(username=username,password=password)
        if not user:
            raise forms.ValidationError("Invalid username or password")
        cleaned_data['user']=user
        print("user authenticated", cleaned_data)
        return cleaned_data
