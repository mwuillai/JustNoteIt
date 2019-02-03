from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import datetime, timedelta
import pytz
from Project.settings import TIME_ZONE

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
    slug = models.SlugField(max_length=80, null=True, blank=True)
    category_id = models.ManyToManyField("Note.Category")

    class Meta:
        verbose_name = ("Note")
        verbose_name_plural = ("Notes")
        ordering = ("-updated_at", )

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now(pytz.timezone(TIME_ZONE))
        self.slug = slugify(
            f"{self.title}-{self.created_at.day}-{self.created_at.month}-{self.created_at.year}".lower())
        super(Notes, self).save(*args, **kwargs) # Call the real save() method


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
    slug = models.SlugField(max_length=80, null=True, blank=True)

    class Meta:
        verbose_name = ("Category")
        verbose_name_plural = ("Categories")
        ordering = ("-updated_at", )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.title}-{self.created_at.day}-{self.created_at.month}-{self.created_at.year}".lower())
            super(Category, self).save(*args, **kwargs) # Call the real save() method