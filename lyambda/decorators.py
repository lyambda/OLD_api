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
            session = self.db.sessions.find_one({'token' : kwargs['session_token']})

            if session is None:
                return {'ok' : False, 'description' : 'Session not found'}

            if not session['is_authorized'] and is_auth:
                return {'ok' : False, 'description' : 'Session is not authorized'}

            return func(self, *args, **kwargs)

        return wrapper

    return decorator