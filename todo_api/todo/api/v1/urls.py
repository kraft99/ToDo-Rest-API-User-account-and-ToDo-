from django.contrib import admin
from django.urls import path
from . import views


app_name    = 'todo_api'

urlpatterns = [
    path('todos/',views.TodoListCreateAPIView.as_view(),name='todos'),
    path('todos/<int:pk>/',views.TodoRetrieveUpdateDestroyAPIView.as_view(),name='todo-detail'),
]
