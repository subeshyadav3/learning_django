from django.db import models

# Create your models here.
class StudentModel(models.Model):
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    gpa=models.FloatField()
    gmail=models.EmailField(unique=True)

    def __str__(self):
        return self.name
    

