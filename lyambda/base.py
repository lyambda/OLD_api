import abc
import random

from .decorators import (
    check_args,
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

from .utils import Utilities

import datetime

class BaseMethodsAPI(abc.ABC):
    @check_args(['email'], [], {'email' : str})
    def sendCode(self, email):
        try:
            Utilities.delete_not_auth_sesion(email)

            session = Session(
                email=email,
                code=random.randint(100000, 999999),
                token=Utilities.generate_token(),
                is_auth=False
            )

            session.save()
            Utilities.emailt(email, session.code, self.smtp)

            return Utilities.make_reponse(200)
        except ValidationError:
            return Utilities.make_reponse(400, 'Invalid email')

    @check_args(['email', 'code'], [], {'email' : str, 'code' : int})
    def signIn(self, email, code):
        try:
            session = Session.objects.get(email=email, is_auth=False)
        except DoesNotExist:
            return Utilities.make_reponse(404, 'No login required')

        time_wait = datetime.datetime.utcnow() - session.date

        if time_wait.seconds >= 60 * 5 or session.is_auth:
            return Utilities.make_reponse(410, 'The waiting time has expired')

        if session.code != code:
            return Utilities.make_reponse(400, 'Incorrect code')

        try:
            user = User.objects.get(email=session.email)

            session.is_auth = True
            session.id_user = user.id
            session.save()

            return Utilities.make_reponse(200, 'You are logged in', **{
                'is_auth' : True,
                'token' : session.token
            })
        except DoesNotExist:
            return Utilities.make_reponse(200, 'Register now', **{
                'is_auth' : False,
                'token' : session.token
            })

    @check_args(['token', 'name'], ['surname', 'description'], {'token' : str, 'name' : str, 'surname' : str, 'description' : str})
    @check_token()
    def register(self, token, name, surname=None, description=None):
        session = Session.objects.get(token=token)
        time_wait = datetime.datetime.utcnow() - session.date

        if session.is_auth:
            return Utilities.make_reponse(410, 'You are already registered')

        if time_wait.seconds >= 60 * 5:
            return Utilities.make_reponse(400, 'The waiting time has expired')

        user = User(
            email=session.email,
            name=name,
            surname=surname,
            description=description,
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
            return Utilities.make_reponse(400, 'Invalid parameters')

        return Utilities.make_reponse(200, 'Are you registered')

    @check_args(['token'], [], types={'token' : str})
    @check_token(is_auth=True)
    def logOut(self, token):
        Session.objects.get(token=token).delete()

        return Utilities.make_reponse(200)
