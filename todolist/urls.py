from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name='index'),
    path('addtask', views.addtask, name='addtask'),
    path('todolist/<id>/', views.todoDetails, name = 'todolist'),
    path('todoDel/<id>/', views.todoDel, name='todoDel'),
    path('edittask/<id>/', views.edittask, name='edittask'),
    

    
]