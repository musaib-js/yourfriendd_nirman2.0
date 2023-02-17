from django.contrib import admin
from . models import Post, Appointment,SelfCare,Contact
# Register your models here.
admin.site.register((Post, Appointment,SelfCare,Contact))