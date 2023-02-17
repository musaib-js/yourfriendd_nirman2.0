from tabnanny import verbose
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe

#Abstract User Model
class User(AbstractUser):
    is_patient = models.BooleanField('Patient Status', default=False)
    is_consultant = models.BooleanField('Consultant Status', default=False)

#Patient Model
class Patient(models.Model):
    user = models.OneToOneField(User, related_name="user", on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length = 350, default = "patient")
    age = models.IntegerField(default = 00)
    gender = models.CharField(max_length=6, default = "not-specfied")
    history = models.CharField(max_length = 500, default = "None")

    def __str__(self):
        return self.name

#Consultant Model
class Consultant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=250, default = "doctor")
    qualification = models.CharField(max_length = 100)
    speciality = models.CharField(max_length = 300)
    clinic = models.CharField(max_length = 300)
    contact = models.CharField(max_length = 13)
    email = models.EmailField(max_length = 200)
    photo = models.ImageField(upload_to = 'media', default = 'one.jpg')
    bio = models.TextField()

    def __str__(self):
        return self.name

class Subscription_Packs(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 200,unique=True)
    period = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    benefits = models.TextField()
    photo = models.ImageField(upload_to = 'media', default = 'one.jpg')

    class Meta:
        verbose_name_plural = "Subscription Packs"

    def __str__(self):
        return self.name

class Subscribed_Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription_type = models.ForeignKey(Subscription_Packs, on_delete=models.CASCADE, default=None)
    created_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = "Subscribed Users"

    def __str__(self):
        return str(self.user)
    

    
    
    

    

    