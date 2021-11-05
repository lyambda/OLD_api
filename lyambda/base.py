import abc
import random

from .utils import Utilities

from .decorators import (
    required_args,
    check_token
)

from .models import (
    Session,
    User,
    Group,
    Message
)

from mongoengine import (
    ValidationError,
    DoesNotExist
)

import datetime

class BaseMethodsAPI(abc.ABC):
    @required_args(['email'], types={'email' : str})
    def sendCode(self, **args):
        try:
            Utilities.delete_not_auth_sesion(args['email'])

            session = Session(
                email=args['email'],
                code=random.randint(100000, 999999),
                token=Utilities.generate_token(),
                is_auth=False
            )

            session.save()
            Utilities.emailt(args['email'], session.code, self.smtp)

            return {'ok' : True}
        except ValidationError:
            return {'ok' : False, 'error_code' : 400, 'description' : 'Invalid email'}

    @required_args(['email', 'code'], types={'email' : str, 'code' : int})
    def signIn(self, **args):
        try:
            session = Session.objects.get(email=args['email'], is_auth=False)
        except DoesNotExist:
            return {'ok' : False, 'error_code' : 404, 'description' : 'No login required'}, 404

        time_wait = datetime.datetime.utcnow() - session.date

        if time_wait.seconds >= 60 * 5 or session.is_auth:
            return {'ok' : False, 'error_code' : 410, 'description' : 'The waiting time has expired'}, 410

        if str(session.code) != args['code']:
            return {'ok' : False, 'error_code' : 400, 'description' : 'Incorrect code'}, 400

        try:
            user = User.objects.get(email=session.email)

            session.is_auth = True
            session.id_user = user.id
            session.save()

            return {'ok' : True, 'is_auth' : True, 'description' : 'You are logged in', 'token' : session.token}, 200
        except DoesNotExist:
            return {'ok' : True, 'is_auth' : False, 'description' : 'Register now', 'token' : session.token}, 200

    @required_args(['token', 'name'], types={'token' : str, 'name' : str})
    @check_token()
    def register(self, **args):
        session = Session.objects.get(token=args['token'])
        time_wait = datetime.datetime.utcnow() - session.date

        if session.is_auth:
            return {'ok' : False, 'error_code' : 410, 'description' : 'You are already registered'}, 410

        if time_wait.seconds >= 60 * 5:
            return {'ok' : False, 'error_code' : 400, 'description' : 'The waiting time has expired'}, 400

        user = User(
            email=session.email,
            name=args['name'],
            surname=args.get('surname'),
            description=args.get('description'),
        )

        user.groups = [user.id]

        favorites = Group(
            name='Избранное',
            admins=[user.id],
            participants=[user.id],
            is_private=True
        )

        message = Message(
            id_group=favorites.id,
            from_id=user.id,
            text='Сохраняй сюда сообщения друг)))',
        )

        session.is_auth = True
        session.id_user = user.id

        try:
            user.save()
            favorites.save()
            message.save()
            session.save()
        except ValidationError:
            return {'ok' : False, 'error_code' : 400, 'description' : 'Invalid parameters'}, 400

        return {'ok' : True, 'description' : 'Are you registered'}, 200

    @required_args(['token'], types={'token' : str})
    @check_token(is_auth=True)
    def logOut(self, **args):
        Session.objects.get(token=args['token']).delete()

        return {'ok' : True}, 200

        