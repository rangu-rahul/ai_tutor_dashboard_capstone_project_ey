from django.db import models


from django.contrib.auth.models import User
# Create your models here.

class StudentProfiles(models.Model):
    
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    cpassword = models.CharField(max_length=100)
    
    
    def __str__(self):
        return f"{self.user.username}"
    
class FacultyProfiles(models.Model):
    
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    cpassword = models.CharField(max_length=100)
    
    
    def __str__(self):
        return f"{self.user.username}"