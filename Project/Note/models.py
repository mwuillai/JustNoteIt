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
    category_id = models.ManyToManyField("Note.Category", blank=True)

    class Meta:
        verbose_name = ("Note")
        verbose_name_plural = ("Notes")
        ordering = ("-updated_at", )

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """
        If there is no pk it means that is the first time we save this object
        in that case we save it a first time to generate pk and created date.
        In all case after each save we generate a slug in case there is a change in the title
        """
        if not self.pk:
            super(Notes, self).save(*args, **kwargs) 
        self.slug = slugify(
            "-".join([
                self.title,
                str(self.created_at.day),
                str(self.created_at.month),
                str(self.created_at.year),
                str(self.pk)]))
        super(Notes, self).save(*args, **kwargs) # Call the real save() method


class Category(models.Model):
    """
    Class of the category model. they can have a tittle.
    Many notes can be attach to a category, and only one user can be attach to it.
    TODO there is a proble with many to many fields. I have to attach in two way my categories to my note
    I have to see how to solve this and set up test to avoid this problem
    """

    title = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    notes_id = models.ManyToManyField(Notes, blank = True)
    slug = models.SlugField(max_length=80, null=True, blank=True)

    class Meta:
        verbose_name = ("Category")
        verbose_name_plural = ("Categories")
        ordering = ("-updated_at", )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Category, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(
                "-".join([
                    self.title,
                    str(self.created_at.day),
                    str(self.created_at.month),
                    str(self.created_at.year),
                    str(self.pk)
                ]))
        super(Category, self).save(*args, **kwargs) # Call the real save() method