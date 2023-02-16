from urllib.request import Request
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Post
from accounts.models import Consultant, Subscribed_Users, Subscription_Packs
from django.contrib.auth.decorators import login_required
from .models import Appointment
from .models import Post
from datetime import timedelta, datetime
from django.contrib import messages

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        subuser = Subscribed_Users.objects.get(user = request.user)
        if subuser:
            sub_date = subuser.created_at
            pack = Subscription_Packs.objects.get(name = subuser.subscription_type).period
            new_date = sub_date + timedelta(days = pack)
            now = datetime.now()
            current_date = now.date()
            if new_date < current_date:
                subuser.delete()
                messages.success(request, "Your subscription pack has expired")
    post = Post.objects.all()[0:3]
    consultant= Consultant.objects.all()[0:3]
    context = {'post':post, 'consultant':consultant}
    return render(request, 'index.html', context)

def blog(request):
    return render(request, 'blog.html')

def blogpost(request, slug):
    post = Post.objects.filter(slug = slug).first()
    context = {'post':post}
    return render(request, 'blogpost.html', context)

def contact(request):
    if request.method == 'POST':
        pass
    elif request.method =='GET':
        return render(request,'contact.html')
