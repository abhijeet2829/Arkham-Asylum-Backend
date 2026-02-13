import threading
from rest_framework_simplejwt.authentication import JWTAuthentication

_thread_locals = threading.local()

def get_current_user():
    return getattr(_thread_locals, 'user', None)


class ThreadLocalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        if not user or user.is_anonymous:
            try:
                auth = JWTAuthentication()
                res = auth.authenticate(request)
                if res:
                    user = res[0]
                    request.user = user 
            except Exception:
                pass
        
        _thread_locals.user = user
        response = self.get_response(request)
        return response