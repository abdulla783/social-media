from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    desc = models.TextField(null=True, blank=True)
    image = models.ImageField(blank=True, null=True)
    likes = models.ManyToManyField(User, blank=True, related_name='user_likes')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.desc
