import abc
import random

from .utils import (
    generate_token
)

from .decorators import (
    required_args,
    check_token
)

from .models import (
    Session,
    User
)

from mongoengine import (
    ValidationError,
    DoesNotExist
)

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
import smtplib
import os

class BaseMethodsAPI(abc.ABC):
    def _emailt(self, email, code):
        env = Environment(loader=FileSystemLoader('%s/html/' % os.path.dirname(__file__)))
        template = env.get_template('new.html')
        output = template.render(data={'code' : code, 'mail' : email})

        message = MIMEMultipart()

        message['From'] = self.smtp['email']
        message['To'] = email
        message['Subject'] = "Lamda"

        message.attach(MIMEText(output, 'html'))

        server = smtplib.SMTP(f'{self.smtp["host"]}: {self.smtp["port"]}')
        server.starttls()
        server.login(self.smtp['email'], self.smtp['password'])
        server.sendmail(message['From'], message['To'], message.as_string())
        server.quit()

    @required_args(['email'])
    def sendCode(self, **args):
        email = args['email']

        try:
            session = Session(
                email=email,
                code=random.randint(100000, 999999),
                token=generate_token(),
                is_authorized=False
            )

            session.save()
            self._emailt(email, session.code)

            return {'ok' : True, 'session_token' : session.token}
        except ValidationError:
            return {'ok' : False, 'error_code' : 400, 'description' : 'Invalid email'}

    @required_args(['session_token', 'code', 'name'])
    @check_token()
    def register(self, **args):
        session = Session.objects.get(token=args['session_token'])

        try:
            user = User.objects.get(email=session.email)
            return {'ok' : False, 'error_code' : 400, 'description' : 'You are already registered'}
        except DoesNotExist:
            pass

        if session.is_authorized:
            return {'ok' : False, 'error_code' : 400, 'description' : 'The session is already authorized'}
        elif str(session.code) != args['code']:
            return {'ok' : False, 'error_code' : 400, 'description' : 'Incorrect code'}

        user = User(
            email=session.email,
            name=args['name'],
            surname=args.get('surname'),
            description=args.get('description'),
        )

        session.is_authorized = True
        session.code = None
        session.id_user = user.id

        try:
            user.save()
            session.save()
        except ValidationError:
            return {'ok' : True, 'error_code' : 400, 'description' : 'Invalid parameters'}

        return {'ok' : True, 'description' : 'Are you registered'}

    @required_args(['session_token', 'code'])
    @check_token()
    def login(self, **args):
        session = Session.objects.get(token=args['session_token'])

        try:
            user = User.objects.get(email=session.email)
        except DoesNotExist:
            return {'ok' : False, 'error_code' : 400, 'description' : 'You are not registred'}

        if str(session.code) != args['code']:
            return {'ok' : False, 'error_code' : 400, 'description' : 'Incorrect code'}
        elif session.is_authorized:
            return {'ok' : False, 'error_code' : 400, 'description' : 'The session is already authorized'}

        session.is_authorized = True
        session.code = None
        session.id_user = user.id

        session.save()

        return {'ok' : True, 'description' : 'You are logged in'}

    @required_args(['session_token'])
    @check_token(is_auth=True)
    def logOut(self, **args):
        Session.objects.get(token=args['session_token']).delete()

        return {'ok' : True}

        