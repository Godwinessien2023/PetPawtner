from django.contrib import admin
from .models import Profile, Pet, Vet, Post, Like

"""
Register the Profile model to the admin site
"""
admin.site.register(Profile)
admin.site.register(Pet)
admin.site.register(Vet)
admin.site.register(Post)
admin.site.register(Like)
