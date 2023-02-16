from django.contrib import admin
from .models import User, Patient, Consultant, Subscription_Packs, Subscribed_Users
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'is_patient', 'is_consultant']
    fieldsets = (
        (None, {'fields': ('username', 'password', 'is_patient', 'is_consultant')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
        
admin.site.register(User, CustomUserAdmin)
admin.site.register((Patient, Consultant, Subscription_Packs, Subscribed_Users))

admin.site.site_header  =  "Your Friendd Adminstration"  
admin.site.site_title  =  "Your Friendd"
admin.site.index_title  =  "Your Friendd"