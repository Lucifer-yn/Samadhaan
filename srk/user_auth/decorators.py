from django.shortcuts import redirect

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if "admin_id" not in request.session:
            return redirect("admin_login")  # Redirect to Admin Login if not authenticated
        return view_func(request, *args, **kwargs)
    return wrapper
