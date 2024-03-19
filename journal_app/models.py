from django.db import models

# Create your models here.


class Journal(models.Model):
    """Handles User Journals, Users can have multiple Journals"""
    title = models.CharField(max_length=200, blank=False)
    author_name = models.CharField(max_length=200, blank=False)
    memo = models.TextField(max_length=500)
    is_public = models.BooleanField(default=False)
    journal_icon = models.ImageField(upload_to='uploads/journal_icons')
