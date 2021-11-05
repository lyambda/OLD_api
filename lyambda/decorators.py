from .models import Session
from mongoengine import DoesNotExist

def required_args(req_args, types):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            for arg in req_args:
                if arg in kwargs.keys():
                    try:
                        types[arg](kwargs[arg])
                    except ValueError:
                        return {'ok' : False, 'error_code' : 400, 'description' : 'Invalid parameters'}, 400
                else:
                    return {'ok' : False, 'error_code' : 400, 'description' : 'Invalid parameters'}, 400

            return func(self, *args, **kwargs)

        return wrapper

    return decorator

def check_token(is_auth=False):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                session = Session.objects.get(token=kwargs['token'])

                if is_auth and not session.is_auth:
                    return {'ok' : False, 'error_code' : 403, 'description' : 'Session is not authorized'}, 403
            except DoesNotExist:
                return {'ok' : False, 'error_code' : 404, 'description' : 'Session not found'}, 404

            return func(self, *args, **kwargs)

        return wrapper

    return decorator