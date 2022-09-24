from django.db import models
import datetime
import requests
import base64

from django.contrib.auth.models import User

from .choices import RelationshipChoice


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True, related_name="profile")
    profile_image = models.ImageField(blank=True, null=True)
    cover_image = models.ImageField(blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='user_followers',
                                    blank=True)
    following = models.ManyToManyField(User, related_name='user_following',
                                    blank=True)
    dob = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)

    about = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    full_address = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=7, null=True, blank=True)
    relationship = models.CharField(max_length=50, choices=RelationshipChoice.choices, default="none")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


        
        
