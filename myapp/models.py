from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tarea(models.Model):
    title = models.CharField( max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=50)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)