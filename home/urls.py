from django.urls import path, include
from. import views


urlpatterns = [
    path('', views.home, name = "home"),
    # path('about/', views.about, name = "about"),
    path('blog/', views.blog, name = "blog"),
    path('blog/<str:slug>/', views.blogpost, name = "blogpost"),
    path('contact/',views.contact,name='contact'),
]