from django.urls import path
from . import views


"""
add url patterns as will be used in the view.py
"""
urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('signup/', views.signup, name='signup'),  # User signup
    path('settings/', views.settings, name='settings'),  # User settings
    path('add_pets/', views.add_pets, name='add_pets'),  # Add pets page
    path('signin/', views.signin, name='signin'),  # User signin
    path('signout/', views.signout, name='signout'),  # User signout
]
