from django.shortcuts import render, redirect
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


def list_journals_own(request):
    """Lists all journals owned by the requestor (TODO authorization not impl yet)"""
    context = {}

    context["journals"] = Journal.objects.all()

    return render(request, "authed/list_journals_own.html", context)


def detail_journal(request):
    """Shows details about a specific journal"""
    context = {}

    journal_id = request.GET.get("id", False)

    # Guard clause if no id provided
    if not journal_id:
        # TODO modify list_journals to popup a warning if this happens
        redirect('/public?invalid_id=1')

    # Begin logic branch
    try:
        context["journal"] = Journal.objects.get(id=journal_id)
        return render(request, "public/detail_journal.html", context)

    except Journal.DoesNotExist:
        return redirect('/public?invalid_id=1')
