from django.db import models
class GeeksManager(models.Manager):
    def by_title(self, title):
        return self.filter(title=title)

class GeeksModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    objects = GeeksManager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'geeks_table'
        ordering = ['title']


