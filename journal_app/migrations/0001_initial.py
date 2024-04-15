# Generated by Django 4.2 on 2024-04-15 20:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author_name', models.CharField(max_length=200)),
                ('memo', models.TextField(max_length=500)),
                ('is_public', models.BooleanField(default=False)),
                ('journal_icon', models.ImageField(default='defaults/journal_icon.svg', upload_to='uploads/journal_icons')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField(max_length=500)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('journal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='journal_app.journal')),
            ],
        ),
    ]
