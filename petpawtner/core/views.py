from django.shortcuts import render
from django.http import HttpResponse


"""Define an index function that returns HttpResponse as
indicated in the core/urls.py file.
"""
def index(request):
    return render(request, 'index.html')
