from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

#set a variable so User = get_user_model
User = get_user_model()

"""Create a profile class to inherit from the model.Model class
automatically created by Django as default user
and link the user using a FK
"""
class Profile(models.Model):
    USER_ROLES = (
        ('owner', 'Pet Owner'),
        ('vet', 'Vet'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_image', default='dog_paw-pp.png')
    location = models.CharField(max_length=50)
    role = models.CharField(max_length=5, choices=USER_ROLES, default='owner')  # New field to specify the role

    def __str__(self):
        return self.user.username
    
"""
Create a pet class to inherit from the model.Model class
and link the pet to the owner using a FK
"""
class Pet(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='pets')
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.CharField(max_length=20)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='pet_images', default='dog_paw-pp.png')
    location = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.breed}) - {self.owner.user.username}"
    
"""
Create a vet class to inherit from the model.Model class
and link the vet to the profile using a OneToOneField
"""
class Vet(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='vet_profile')
    clinic_name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    years_of_experience = models.IntegerField()
    contact_info = models.CharField(max_length=100, blank=True)
    profileimg = models.ImageField(upload_to='vet_images', default='vet-icon.png')
    location = models.CharField(max_length=50)

    def __str__(self):
        return f"Dr. {self.profile.user.username} - {self.specialty}"

