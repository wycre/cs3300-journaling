from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated(view_func):
    """Makes this view only work for users who are not authenticated"""
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper


def allowed_users(allowed_roles=[]):
    """Only allows users in the list of allowed roles to access this view"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            group = None;

            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)

            else:
                return redirect('login')
        return wrapper
    return decorator
