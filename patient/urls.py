from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('about/',views.about, name='aboutUs'),

    path('hospital/', views.hospital, name='Best Hospital'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),

     path('predict', views.predict, name='predict'),





]
