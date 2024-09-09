from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile, Pet, Vet
from django.contrib.auth.decorators import login_required




def index(request):
    """
    Define an index function that returns HttpResponse (index, the home page) 
    """
    return render(request, 'index.html')

def signup(request):
    """
    Define signup function that returns POST form of signed up user to the database
    """
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

                # Create a profile object for the user
                Profile.objects.create(user=user)  # Create profile with default values

                # Log user in and redirect to settings page
                user_signin = auth.authenticate(username=username, password=password)
                auth.login(request, user_signin)

                # Redirect to settings page for profile completion
                return redirect('settings')  # Redirect to settings page

        else:
            messages.info(request, 'Passwords do not match')
            return render(request, 'signup.html')

    else:
        return render(request, 'signup.html')


@login_required(login_url='signin')
def settings(request):
    """
    Define settings function that returns settings.html where 
    users will fill a form indicating their role, if they are a 
    vet or pet owners upon a successful signup.
    If they are vets, they are redirected to the home page,
    and if they are pet owners, they are redirected to the add_pets page
    where they can add profile of their pets before they are returned to home 
    page
    """
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        role = request.POST.get('role')  # Assuming a form with a 'role' field (owner or vet)
        profile.role = role
        profile.bio = request.POST.get('bio')
        profile.location = request.POST.get('location')
        profile.save()

        if role == 'vet':
            # Collect additional vet information
            clinic_name = request.POST.get('clinic_name')
            specialty = request.POST.get('specialty')
            years_of_experience = request.POST.get('years_of_experience')
            contact_info = request.POST.get('contact_info')

            # Create vet profile
            Vet.objects.create(
                profile=profile,
                clinic_name=clinic_name,
                specialty=specialty,
                years_of_experience=years_of_experience,
                contact_info=contact_info,
            )
            return redirect('index')  # Redirect vets to the home page

        elif role == 'owner':
            return redirect('add_pets')  # Redirect pet owners to the add_pets page

    return render(request, 'settings.html')


@login_required(login_url='signin')
def add_pets(request):
    """
    Create a add_pets function that allows pet owners to add pet details.
    """
    if request.method == 'POST':
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            messages.error(request, 'Profile does not exist.')
            return redirect('settings')

        pet_name = request.POST.get('name')
        pet_breed = request.POST.get('breed')
        pet_age = request.POST.get('age')
        pet_bio = request.POST.get('bio')
        pet_location = request.POST.get('location')
        pet_profileimg = request.FILES.get('profileimg')

        Pet.objects.create(
            owner=profile,
            name=pet_name,
            breed=pet_breed,
            age=pet_age,
            bio=pet_bio,
            profileimg=pet_profileimg,
            location=pet_location,
        )

        return redirect('index')

    return render(request, 'add_pets.html')


def signin(request):
    """
    define signin funtion that returns signin.html upon successfuly
    uthenticating a user
    """
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


@login_required(login_url='signin')
def signout(request):
    """
    define a signout function that logs out a user and redirects
    a user to sign in page
    @login_required(login_url='signin') decorator is used to ensure
    that only authenticated users can sign out
    """
    auth.logout(request)
    return redirect('signin')
