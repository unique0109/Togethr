from django.db import models

# Create your models here.
class Data(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.first_name
    
class SearchHist(models.Model):
    username = models.CharField(max_length=100)
    searchTitle = models.TextField()
    searchRes = models.TextField()

    def __str__(self):
        return self.username