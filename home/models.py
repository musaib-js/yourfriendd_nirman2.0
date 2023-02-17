from functools import partialmethod
from django.db import models
from accounts.models import Consultant, User

# Create your models here.
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title  = models.CharField(max_length = 300)
    author = models.CharField(max_length = 300)
    body = models.TextField()
    timeStamp = models.DateTimeField(auto_now = True)
    slug = models.CharField(max_length = 350)
    tags = models.TextField()

    def __str__(self):
        return self.title + " by " + self.author

class Appointment(models.Model):
    name = models.CharField(max_length = 150)
    age = models.IntegerField()
    patient = models.ForeignKey(User, related_name="patient", on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name="doctor", on_delete=models.CASCADE)
    date = models.DateField()
    meet_link = models.CharField(max_length = 150)
    approved = models.BooleanField(default=False)
    conducted = models.BooleanField(default=False)
    is_rescheduled = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class SelfCare(models.Model):
    name=models.CharField(max_length=255)
    posted_by=models.ForeignKey(User,on_delete=models.CASCADE)
    file=models.FileField(upload_to="selfcare")
    description=models.TextField()

    def __str__(self):
        return self.name

class Contact(models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField()
    subject=models.CharField(max_length=255)
    message=models.TextField()

    def __str__(self):
        return self.email
    
    
