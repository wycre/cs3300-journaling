from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from journal_app.models import Journal, Post


class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ['title', 'author_name', 'memo', 'is_public', 'journal_icon']

    # Make image field not required
    def __init__(self, *args, **kwargs):
        super(JournalForm, self).__init__(*args, **kwargs)
        self.fields['journal_icon'].required = False
        self.fields['memo'].strip = False


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
