from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile


"""Define an index function that returns HttpResponse (index, the home page) as
indicated in the core/urls.py file.
"""
def index(request):
    return render(request, 'index.html')


"""
define signup funcition that returns POST 
form of signed up user to the database
"""
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return render(request, 'signup.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return render(request, 'signup.html')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page

                """
                create a profile object for the user
                """
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('index')


                return render(request, 'index.html')
        else:
            messages.info(request, 'Password does not match')
            return render(request, 'signup')

    else:
        return render(request, 'signup.html')


"""
define signin funtion that returns signin.html
"""
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index') #change this to use experience page
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('signin')
    else:
        return render(request, 'signin.html')
