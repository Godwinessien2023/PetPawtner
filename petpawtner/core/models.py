from django.db import models
from django.contrib.auth import get_user_model

#set a variable so User = get_user_model
User = get_user_model()

"""Create a profile class to inherit from the model.Model class
automatically created by Django as default user
and link the user using a FK
"""
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_image', default='dog_paw-pp.png')
    location = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.user.username
