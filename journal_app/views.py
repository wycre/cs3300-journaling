from django.contrib import messages
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from .decorators import unauthenticated, allowed_users
from django.contrib.auth.decorators import login_required

from journal_app.forms import JournalForm, PostForm, CreateUserForm
from journal_app.models import Journal, Post


# Create your views here.
def index(request):
    return render(request, "public/homepage.html", {"request":request})


def list_journals(request):
    """Lists all public journals"""
    context = {"request":request}

    context["journals"] = Journal.objects.all().filter(is_public=True)

    return render(request, "public/list_journals.html", context)


@login_required(login_url='login')
@allowed_users(['user'])
def list_journals_own(request):
    """Lists all journals owned by the requestor (TODO authorization not impl yet)"""
    context = {"request":request}

    context["journals"] = Journal.objects.all()

    return render(request, "authed/list_journals_own.html", context)


def detail_journal(request):
    """Shows details about a specific journal"""
    context = {"request": request}

    # Handle Journal ID
    journal_id = request.GET.get("id", False)
    if not journal_id:
        # TODO modify list_journals to popup a warning if this happens
        redirect('/public?invalid_id=1')

    # Update context if user is authenticated
    if request.user.is_authenticated:
        context["authed"] = True
    else:
        context["authed"] = False

    # Attempt to render Journal
    try:
        # otherwise send journal details
        context["journal"] = Journal.objects.get(id=journal_id)
        context["posts"] = Post.objects.filter(journal=context["journal"]).order_by('-last_modified')

        return render(request, "public/detail_journal.html", context)

    except Journal.DoesNotExist:
        return redirect('/public?invalid_id=1')


@login_required(login_url='login')
@allowed_users(['user'])
def new_journal(request):
    """Form for creating a Journal"""
    context = {"request":request}

    # TODO: Add User Auth Check for Journal Ownership

    # Make Empty Journal
    if request.method == "GET":
        form = JournalForm()
        context["form"] = form

        return render(request, "authed/forms/journal_create_form.html", context)

    # Handle Filled Journal
    if request.method == "POST":
        form = JournalForm(request.POST, request.FILES)

        # Apply form values to db
        if form.is_valid():
            title = form.cleaned_data["title"]
            author = form.cleaned_data["author_name"]
            memo = form.cleaned_data["memo"]
            is_public = form.cleaned_data["is_public"]
            journal_icon = form.cleaned_data["journal_icon"]  # Will contain default if not provided

            journal = Journal.objects.create(title=title, author_name=author, memo=memo, is_public=is_public,
                                             journal_icon=journal_icon, user=request.user)

            context["journal"] = journal
            return redirect('/journal?id={}'.format(journal.id))

        else:
            context["form"] = form
            return render(request, "authed/forms/journal_create_form.html", context)


@login_required(login_url='login')
@allowed_users(['user'])
def edit_journal(request):
    """Handles editing of journals"""
    context = {"request":request}

    journal_id = request.GET.get("id", False)

    # Guard clause if no id provided
    if not journal_id:
        # TODO modify list_journals to popup a warning if this happens
        redirect('/public?invalid_id=1')

    # POST behavior
    if request.method == "POST":
        form = JournalForm(request.POST, request.FILES)

        try:
            journal = Journal.objects.get(id=journal_id)
            context["journal"] = journal

            # Apply form values to db
            if form.is_valid():
                journal.title = form.cleaned_data["title"]
                journal.author_name = form.cleaned_data["author_name"]
                journal.memo = form.cleaned_data["memo"]
                journal.is_public = form.cleaned_data["is_public"]

                # journal icon is optional
                if request.FILES.get("journal_icon", False):
                    journal.journal_icon = form.cleaned_data["journal_icon"]

                journal.save()

                context["journal"] = journal
                return redirect('/journal?id={}'.format(journal_id))

            else:
                context["form"] = form
                return render(request, "authed/forms/journal_edit_form.html", context)

        except Journal.DoesNotExist:
            return redirect('/public?invalid_id=1')


    # GET behavior
    context["journal"] = Journal.objects.get(id=journal_id)

    form = JournalForm(instance=context["journal"])
    context["form"] = form

    return render(request, "authed/forms/journal_edit_form.html", context)


@login_required(login_url='login')
@allowed_users(['user'])
def delete_journal(request):
    """Form to delete a journal"""
    context = {"request":request}

    journal_id = request.GET.get("id", False)

    # Guard clause if no id provided
    if not journal_id:
        # TODO modify list_journals to popup a warning if this happens
        redirect('/public?invalid_id=1')

    # Begin logic branch
    if request.method == "GET":

        try:
            context["journal"] = Journal.objects.get(id=journal_id)

            form = forms.Form()
            context["form"] = form

            return render(request, "authed/forms/journal_delete_form.html", context)

        except Journal.DoesNotExist:
            return redirect('/public?invalid_id=1')

    if request.method == "POST":
        form = forms.Form(request.POST)

        try:
            journal = Journal.objects.get(id=journal_id)
            context["journal"] = journal

            # Delete form
            if form.is_valid():
                journal.delete()
                return redirect('/public')

        except Journal.DoesNotExist:
            return redirect('/public?invalid_id=1')


def detail_post(request):
    """Shows details about a specific post"""
    context = {"request": request}

    post_id = request.GET.get("p", False)

    # Guard clause if no id provided
    if not post_id:
        # TODO modify list_journals to popup a warning if this happens
        redirect('/public?invalid_p=1')

    # Begin logic branch
    if request.method == "GET":

        try:
            # otherwise send journal details
            context["post"] = Post.objects.get(id=post_id)
            context["journal"] = Journal.objects.get(id=context["post"].journal.id)
            return render(request, "public/detail_post.html", context)

        except Journal.DoesNotExist:
            return redirect('/public?invalid_id=1')


@login_required(login_url='login')
@allowed_users(['user'])
def new_post(request):
    """Makes a new post"""

    context = {"request":request}

    journal_id = request.GET.get("id", False)

    if not journal_id:
        # TODO modify list_journals to popup a warning if this happens
        redirect('/public?invalid_id=1')

    # TODO: Add User Auth Check for Journal Ownership

    # Make Empty Journal
    if request.method == "GET":
        form = PostForm()
        context["form"] = form
        context["journal"] = Journal.objects.get(id=journal_id)

        return render(request, "authed/forms/post_create_form.html", context)

    # Handle Filled Journal
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        # Apply form values to db
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            post = Post.objects.create(title=title, content=content, journal=Journal.objects.get(id=journal_id))

            context["post"] = post
            return redirect('/post?p={}'.format(post.id))

        else:
            context["form"] = form
            return render(request, "authed/forms/post_create_form.html", context)


@login_required(login_url='login')
@allowed_users(['user'])
def edit_post(request):
    """Edits an existing post"""

    context = {"request":request}

    post_id = request.GET.get("p", False)

    if not post_id:
        # TODO modify list_journals to popup a warning if this happens
        redirect('/public?invalid_p=1')

    # TODO: Add User Auth Check for post Ownership

    # Make Empty Journal
    if request.method == "GET":
        context["post"] = Post.objects.get(id=post_id)

        form = PostForm(instance=context["post"])
        context["form"] = form

        return render(request, "authed/forms/post_edit_form.html", context)

    # Handle Filled Journal
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        post = Post.objects.get(id=post_id)

        # Apply form values to db
        if form.is_valid():
            post.title = form.cleaned_data["title"]
            post.content = form.cleaned_data["content"]

            post.save()

            context["post"] = post
            return redirect('/post?p={}'.format(post.id))

        else:
            context["form"] = form
            return render(request, "authed/forms/post_edit_form.html", context)


@login_required(login_url='login')
@allowed_users(['user'])
def delete_post(request):
    """Form to delete a post"""
    context = {"request":request}

    post_id = request.GET.get("p", False)

    # Guard clause if no id provided
    if not post_id:
        # TODO modify list_journals to popup a warning if this happens
        redirect('/public?invalid_p=1')

    # Begin logic branch
    if request.method == "GET":

        try:
            context["post"] = Post.objects.get(id=post_id)

            form = forms.Form()
            context["form"] = form

            return render(request, "authed/forms/post_delete_form.html", context)

        except Post.DoesNotExist:
            return redirect('/public?invalid_p=1')

    if request.method == "POST":
        form = forms.Form(request.POST)

        try:
            post = Post.objects.get(id=post_id)
            context["post"] = post

            # Delete form
            if form.is_valid():
                post.delete()
                return redirect('/public')

        except Journal.DoesNotExist:
            return redirect('/public?invalid_p=1')


@unauthenticated
def register_page(request):
    """User Registration"""

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='user')
            user.groups.add(group)

            print(form.errors)

            messages.success(request, "Account was created for " + username)
            return redirect('login')

        print(form.errors)

    context = {'form': form, "request":request}
    return render(request, 'registration/register.html', context)
