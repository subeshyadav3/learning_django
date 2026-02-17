from django.db import models

# Create your models here.
class Blog(models.Model):
    title=models.CharField(max_length=200)
    blog_body=models.TextField()

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='comments')
    comment_body=models.TextField()

    def __str__(self):
        return self.comment_body[:50]  # Return first 50 characters of the comment