from django.shortcuts import render, redirect
from django.http import HttpResponse

from journal_app.forms import JournalForm
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
    is_editing = request.GET.get("edit", False)

    # Guard clause if no id provided
    if not journal_id:
        # TODO modify list_journals to popup a warning if this happens
        redirect('/public?invalid_id=1')

    # Begin logic branch
    if request.method == "GET":

        try:
            # Generate & return form
            if is_editing:
                context["journal"] = Journal.objects.get(id=journal_id)

                form = JournalForm(instance=context["journal"])
                context["form"] = form

                return render(request, "authed/forms/journal_edit_form.html", context)

            # otherwise send journal details
            context["journal"] = Journal.objects.get(id=journal_id)
            return render(request, "public/detail_journal.html", context)

        except Journal.DoesNotExist:
            return redirect('/public?invalid_id=1')

    if request.method == "POST":
        form = JournalForm(request.POST, request.FILES)

        try:
            journal = Journal.objects.get(id=journal_id)
            context["journal"] = journal

            # Apply form values to db
            if form.is_valid():
                journal.title = form.cleaned_data["title"]
                journal.author = form.cleaned_data["author_name"]
                journal.memo = form.cleaned_data["memo"]
                journal.is_editing = form.cleaned_data["is_public"]

                # journal icon is optional
                if form.cleaned_data["journal_icon"]:
                    journal.journal_icon = form.cleaned_data["journal_icon"]

                journal.save()

                context["journal"] = journal
                return redirect('/journal?id={}'.format(journal_id))

            else:
                context["form"] = form
                return render(request, "authed/forms/journal_edit_form.html", context)

        except Journal.DoesNotExist:
            return redirect('/public?invalid_id=1')

