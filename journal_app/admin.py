from django.contrib import admin

from journal_app.models import Journal, Post

# Register your models here.
admin.site.register(Journal)
admin.site.register(Post)