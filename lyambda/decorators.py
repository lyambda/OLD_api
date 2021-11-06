from .models import Session
from .utils import Utilities
from mongoengine import DoesNotExist

def check_args(required_args: list[str], optional_args: list[str], types: dict[str, tuple[type]]):
    def decorator(func):
        def wrapper(*_, **args):
            for arg in required_args:
                if arg not in args or not isinstance(args[arg], types[arg]):
                    return Utilities.make_reponse(400, 'Invalid parameters')

            for arg in args:
                if (arg not in optional_args and arg not in required_args) or not isinstance(args[arg], types[arg]):
                    return Utilities.make_reponse(400, 'Invalid parameters')

            return func(*_, **args)

        return wrapper

    return decorator

def check_token(is_auth=False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                session = Session.objects.get(token=kwargs['token'])

                if is_auth and not session.is_auth:
                    return Utilities.make_reponse(403, 'Session is not authorized')
            except DoesNotExist:
                return Utilities.make_reponse(404, 'Session not found')

            return func(*args, **kwargs)

        return wrapper

    return decorator