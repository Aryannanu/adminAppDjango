from django.shortcuts import redirect
from .jwt_utils import decode_jwt
from .models import AppUser

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get('jwt_token')
        if not token:
            return redirect('login_view')

        payload = decode_jwt(token)
        if not payload:
            return redirect('login_view')
        try:
            request.current_user = AppUser.objects.get(id=payload['user_id'])
        except AppUser.DoesNotExist:
            return redirect('login_view')

        return view_func(request, *args, **kwargs)
    return wrapper
