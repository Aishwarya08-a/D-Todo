from django.contrib import admin
from django.urls import path
from todoapp import views

urlpatterns = [
    path('signup',views.user_signup),
    path('login',views.user_login),
    path('home',views.home),
    path('add', views.add),
    path('delete/<int:todo_id>/', views.delete),
    path('complete/<int:todo_id>/', views.complete),
]