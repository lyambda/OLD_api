from .models import Session
from mongoengine import DoesNotExist

def required_args(req_args):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            for arg in req_args:
                if arg not in kwargs.keys():
                    return {'ok' : False, 'description' : 'Invalid arguments'}

            return func(self, *args, **kwargs)

        return wrapper

    return decorator

def check_token(is_auth=False):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                session = Session.objects.get(token=kwargs['token'])

                if is_auth and not session.is_auth:
                    return {'ok' : False, 'error_code' : 401, 'description' : 'Session is not authorized'}
            except DoesNotExist:
                return {'ok' : False, 'error_code' : 400, 'description' : 'Session not found'}

            return func(self, *args, **kwargs)

        return wrapper

    return decorator