from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(views_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                if group == 'customers':
                    return redirect('store')
                else:
                    return redirect('ware')
        else:
            return views_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('No Tiene los Privilegios para Acceder a esta Pagina!\nQUE LASTIMA!')

        return wrapper_func

    return decorator
