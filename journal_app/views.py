from django.shortcuts import render
from django.http import HttpResponse

from journal_app.models import Journal


# Create your views here.
def index(request):
    return render(request, "public/homepage.html", {})


def list_journals(request):
    """Lists all public journals"""
    context = {}

    context["journals"] = Journal.objects.all().filter(is_public=True)

    return render(request, "public/list_journals.html", context)
