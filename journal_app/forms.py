from django import forms

from journal_app.models import Journal


class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ['title', 'author', 'memo', 'is_public', 'journal_icon']