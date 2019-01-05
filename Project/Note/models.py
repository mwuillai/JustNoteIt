from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Notes(models.Model):
    """
    Class of the notes model. they can have a body and a tittle.
    Many categories can be attach to a notes, and only one user can be attach to it.
    """
    title = models.CharField(max_length=30)
    body = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=1)


class Category(models.Model):
    """
    Class of the category model. they can have a tittle.
    Many notes can be attach to a category, and only one user can be attach to it.
    """
    title = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    notes_id = models.ManyToManyField(Notes)
