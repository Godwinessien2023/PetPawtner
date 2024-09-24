from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


"""
add url patterns as will be used in the view.py
"""
urlpatterns = [
    path('', views.index, name='index'),  # Landng page
    path('home/', views.home, name='home'),  # Home page
    path('signup/', views.signup, name='signup'),  # User signup
    path('settings/', views.settings, name='settings'),  # User settings
    path('profile/<str:pk>', views.profile, name='profile'),  # profile
    path('add_pets/', views.add_pets, name='add_pets'),  # Add pets page
    path('signin/', views.signin, name='signin'),  # User signin
    path('signout/', views.signout, name='signout'),  # User signout
    path('search/', views.search, name='search'), # Search page
    path('post/', views.post, name='post'), # Post page
    path('like_post/', views.like_post, name='like_post') # Like post
]
