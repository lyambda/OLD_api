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
import datetime
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

    def _delete_not_auth_sesion(self, email):
        try:
            session = Session.objects.get(email=email, is_auth=False)
            session.delete()
        except DoesNotExist:
            pass

    @required_args(['email'])
    def sendCode(self, **args):
        try:
            self._delete_not_auth_sesion(args['email'])

            session = Session(
                email=args['email'],
                code=random.randint(100000, 999999),
                token=generate_token(),
                is_auth=False
            )

            session.save()
            self._emailt(args['email'], session.code)

            return {'ok' : True}
        except ValidationError:
            return {'ok' : False, 'error_code' : 400, 'description' : 'Invalid email'}

    @required_args(['email', 'code'])
    def signIn(self, **args):
        try:
            session = Session.objects.get(email=args['email'], is_auth=False)
        except DoesNotExist:
            return {'ok' : False, 'error_code' : 404, 'description' : 'No login required'}

        time_wait = datetime.datetime.utcnow() - session.date

        if time_wait.seconds >= 60 * 5 or session.is_auth:
            return {'ok' : False, 'error_code' : 410, 'description' : 'The waiting time has expired'}

        if str(session.code) != args['code']:
            return {'ok' : False, 'error_code' : 400, 'description' : 'Incorrect code'}

        try:
            user = User.objects.get(email=session.email)

            session.is_auth = True
            session.id_user = user.id
            session.save()

            return {'ok' : True, 'is_auth' : True, 'description' : 'You are logged in', 'token' : session.token}
        except DoesNotExist:
            return {'ok' : True, 'is_auth' : False, 'description' : 'Register now', 'token' : session.token}

    @required_args(['token', 'name'])
    @check_token()
    def register(self, **args):
        session = Session.objects.get(token=args['token'])
        time_wait = datetime.datetime.utcnow() - session.date

        if session.is_auth:
            return {'ok' : False, 'error_code' : 410, 'description' : 'You are already registered'}

        if time_wait.seconds >= 60 * 5:
            return {'ok' : False, 'error_code' : 400, 'description' : 'The waiting time has expired'}

        user = User(
            email=session.email,
            name=args['name'],
            surname=args.get('surname'),
            description=args.get('description'),
        )

        session.is_auth = True
        session.id_user = user.id

        try:
            user.save()
            session.save()
        except ValidationError:
            return {'ok' : True, 'error_code' : 400, 'description' : 'Invalid parameters'}

        return {'ok' : True, 'description' : 'Are you registered'}

    @required_args(['token'])
    @check_token(is_auth=True)
    def logOut(self, **args):
        Session.objects.get(token=args['token']).delete()

        return {'ok' : True}

        