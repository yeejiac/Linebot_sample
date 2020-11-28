from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
 
urlpatterns = [
    path('callback', views.callback)
    path('mylinebot/', include('mylinebot.urls')) #包含應用程式的網址
]