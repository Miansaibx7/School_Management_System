from django.shortcuts import redirect
from django.contrib import messages

# Decorator for admin
def admin_required(view_func):

    def wrapper(request, *args, **kwargs):

        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        if request.user.is_admin:
            return view_func(request, *args, **kwargs)

        messages.error(request," Access Denied! You don't have permission to access this section.")
        return redirect("dashboard")
    return wrapper



def accountant_required(view_func):

    def wrapper(request, *args, **kwargs):

        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        if request.user.is_accountant:
            return view_func(request, *args, **kwargs)

        messages.error(request," Access Denied! You don't have permission to access this section.")
        return redirect("dashboard")
    return wrapper