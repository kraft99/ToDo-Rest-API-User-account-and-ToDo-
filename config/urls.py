
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/',include('todo_api.todo.api.v1.urls',namespace='todo_api')),
    path('api/v1/',include('todo_api.account.api.v1.urls',namespace='account_api')),

]
