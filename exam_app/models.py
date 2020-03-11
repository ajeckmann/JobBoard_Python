from __future__ import unicode_literals
from django.db import models
import re




class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors={}
        if len(postData['firstname'])<2:
            errors["firstname"]="First Name should contain at least 2 characters"
        if len(postData['lastname'])<2:
            errors["lastname"]= "Last Name should have at least 2 characters"
        if len(postData['password'])<8:
            errors["password"]="Password must be at least 8 characters"
        if len(User.objects.filter(email=postData['email']))!=0:
            errors['email_in_use']="Sorry, email already in use"
        if postData['confirmpassword']!=postData['password']:
            errors["confirmpassword"]= "Passwords do not match."
        EMAIL_REGEX= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email']=("Invalid email address!")
        return errors

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
  
# Create your models here.


class JobManager(models.Manager):
    def basic_validator(self, postData):
        errors={}
        if len(postData['title'])<3:
            errors["title"]="Title needs to have at least 3 characters"
        if len(postData['description'])<3:
            errors["description"]="Description needs to have at least 3 characters"
        if len(postData['location'])<3:
            errors["location"]="Location needs to have at least 3 characters"
        return errors
        
class Job(models.Model):
    title=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    location=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user=models.ForeignKey(User, related_name="jobs", on_delete = models.CASCADE)
    assigned=models.ForeignKey(User, related_name="assignedjobs", null=True, on_delete = models.CASCADE)
    objects=JobManager()
