# Generated by Django 4.2 on 2024-04-19 19:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('journal_app', '0002_journal_user_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
