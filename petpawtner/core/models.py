from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import uuid
from datetime import datetime

User = get_user_model()


class Profile(models.Model):
    """Create a profile class to inherit from the model.Model class
    automatically created by Django as default user
    and link the user using a FK
    """
    USER_ROLES = (
        ('owner', 'Pet Owner'),
        ('vet', 'Vet'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_image', default='dog_paw-pp.png')
    location = models.CharField(max_length=50)
    role = models.CharField(max_length=5, choices=USER_ROLES, default='owner')

    def __str__(self):
        return self.user.username
    

class Pet(models.Model):
    """
    Create a pet class to inherit from the model.Model class
    and link the pet to the owner using a FK
    """
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='pets')
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.CharField(max_length=20)
    sex = models.CharField(max_length=10, default='Unknown')
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='pet_images', default='dog_paw-pp.png')
    location = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.breed}) - {self.owner.user.username}"
    

class Vet(models.Model):
    """
    Create a vet class to inherit from the model.Model class
    and link the vet to the profile using a OneToOneField
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='vet_profile')
    clinic_name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    years_of_experience = models.IntegerField()
    contact_info = models.CharField(max_length=100, blank=True)
    profileimg = models.ImageField(upload_to='vet_images', default='vet-icon.png')
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    """
    Create a post class to inherit from the model.Model class
    and link the post to the Pets
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    caption = models.TextField(max_length=300)
    no_of_likes = models.IntegerField(default=0)
    image = models.ImageField(upload_to='post_images')
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.user.username)

class Like(models.Model):
    """
    Create a like class to inherit from the model.Model class
    and link the like to the post
    """
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return str(self.username)

class Message(models.Model):
    """
    Model to represent messages exchanged between users (vet or pet owner).
    """
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  

    def __str__(self):
        return f"Message from {self.sender.user.username} to {self.receiver.user.username} at {self.timestamp}"

