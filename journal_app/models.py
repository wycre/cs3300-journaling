from django.db import models
from prose.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.


class Journal(models.Model):
    """Handles User Journals, Users can have multiple Journals"""
    title = models.CharField(max_length=200, blank=False)
    author_name = models.CharField(max_length=200, blank=False)
    memo = models.TextField(max_length=500, blank=False)
    is_public = models.BooleanField(default=False)
    journal_icon = models.ImageField(upload_to='uploads/journal_icons', default='defaults/journal_icon.svg')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


class Post(models.Model):
    """A Post in a Journal"""
    title = models.CharField(max_length=200, blank=False)
    content = RichTextField()
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, blank=False)
    last_modified = models.DateTimeField(auto_now=True)
