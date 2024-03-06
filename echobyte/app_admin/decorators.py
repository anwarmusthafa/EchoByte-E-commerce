from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def custom_user_passes_test(test_func, login_url='admin_login', redirect_field_name=None):
    """
    Decorator for views that checks whether a user passes the given test,
    redirecting to the admin_login page if necessary.
    """
    actual_decorator = user_passes_test(
        test_func,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(login_url)
            return actual_decorator(view_func)(request, *args, **kwargs)
        return _wrapped_view
    return decorator
