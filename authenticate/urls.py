from django.urls import path
from . import views


urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.logon, name='login'),
    path('logout', views.logoutuser, name='logoutuser'),
    path('activateuser/<uidb64>/<token>',views.activateuser, name='activate')
]