from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile, Pet, Vet, Post, Like
from django.contrib.auth.decorators import login_required
import random




def index(request):
    """
    Define an index function that returns HttpResponse (index, the home page) 
    """
    return render(request, 'index.html')

@login_required(login_url='signin')
def home(request):
    """
    Define an home function that returns HttpResponse (home, the app home page)
    """
    users_with_profile = User.objects.filter(profile__profileimg__isnull=False)

    
    user_profile = Profile.objects.get(user=request.user)
    posts = Post.objects.all()
    random_user = random.choice(users_with_profile) if users_with_profile else None

    return render(request, 'home.html', {'user_profile': user_profile, 'posts': posts, 'random_user': random_user})

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
                return redirect('settings')

        else:
            messages.info(request, 'Passwords do not match')
            return render(request, 'signup.html')

    else:
        return render(request, 'signup.html')

@login_required(login_url='signin')
def profile(request, pk):
    """
    Define a profile function that returns profile.html where users can view their profile
    """
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=user_object)
    user_post_len = len(user_posts)

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_len': user_post_len,
    }
    return render(request, 'profile.html', context)


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
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        # Handle the form submission and update the profile
        role = request.POST.get('role')
        bio = request.POST.get('bio')
        location = request.POST.get('location')
        profileimg = request.FILES.get('profileimg')

        # Update the profile
        profile.role = role
        profile.bio = bio
        profile.location = location
        profile.profileimg = profileimg
        
        if role == 'vet':
            profile.clinic_name = request.POST.get('clinic_name')
            profile.specialty = request.POST.get('specialty')
            profile.years_of_experience = request.POST.get('years_of_experience')
            profile.contact_info = request.POST.get('contact_info')

        profile.save()
        messages.success(request, 'Profile updated successfully!')
        
        if role == 'vet':
            return redirect('home')  # Redirect vets to the home page
        elif role == 'owner':
            return redirect('add_pets')  # Redirect pet owners to the add_pets page

    context = {
        'profile': profile,
    }
    return render(request, 'settings.html', context)


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

        return redirect('home')

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
            return redirect('home')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('signin')
    else:
        return render(request, 'signin.html')


@login_required(login_url='signin')
def post(request):
    """
    Allow users to make a post. Pet Owners post about their pets,
    while Vets post general content.
    """
    if request.method == 'POST':
        user = request.user
        image = request.FILES.get('image_upload')
        caption = request.POST.get('caption')

        if not image or not caption:
            messages.error(request, 'Both image and caption are required!')
            return redirect('home')

        try:
            # Save the post
            new_post = Post.objects.create(user=user, image=image, caption=caption)
            new_post.save()
            messages.success(request, 'Post created successfully!')
        except Exception as e:
            print(f"Error saving post: {e}")
            messages.error(request, 'Error saving post!')

        return redirect('home')

    return redirect('home')

@login_required(login_url='signin')
def like_post(request):
    """
    Define a like_post function that allows 
    users to like a post on the app.
    """
    username = request.user.username  # Use the username, not the whole user object
    post_id = request.GET.get('post_id')
    
    # Fetch the post by ID
    post = Post.objects.get(id=post_id)

    # Check if the user has already liked the post
    like_filter = Like.objects.filter(post_id=post_id, username=username).first()
    
    if like_filter is None:  # If no like exists, create a new one
        new_like = Like.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes += 1  # Increment the like count
        post.save()
    else:  # If a like exists, remove it (unlike)
        like_filter.delete()
        post.no_of_likes -= 1  # Decrement the like count
        post.save()
    
    return redirect('home')

@login_required(login_url='signin')
def search(request):
    """
    Define a search function that allows users to search for pets or vets
    """
    query = request.GET.get('q', '')

    pets = []
    vets = []

    if query:
        # Search for pets by name or breed
        pets = Pet.objects.filter(name__icontains=query) | Pet.objects.filter(breed__icontains=query)
        
        # Search for vets by username or specialty
        vets = Vet.objects.filter(specialty__icontains=query)

    context = {
        'pets': pets,
        'vets': vets,
    }
    
    return render(request, 'search.html', context)


@login_required(login_url='signin')
def signout(request):
    """
    define a signout function that logs out a user and redirects
    a user to sign in page
    """
    auth.logout(request)
    return redirect('signin')
