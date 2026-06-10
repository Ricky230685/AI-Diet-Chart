from django.db import models
from django.contrib.auth.models import User

class DietProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    height = models.FloatField()
    weight = models.FloatField()
    goal = models.CharField(max_length=50)
    
    def __str__(self):
        return self.user.username

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    weight = models.FloatField()
    height = models.CharField(max_length=50)
    
    def __str__(self):
        return self.user.username
