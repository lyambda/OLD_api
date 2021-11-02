import abc
import random

from .utils import (
    generate_token,
    get_id
)

from .decorators import (
    required_args,
    check_token
)

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
import smtplib
import os

LENGTH_TOKEN = 32

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

        session = {
            '_id' : get_id(self.db, 'sessions'),
            'id_user' : None,
            'email' : email,
            'code' : random.randint(100000, 999999),
            'token' : generate_token(LENGTH_TOKEN),
            'is_authorized' : False
        }

        self.db.sessions.insert_one(session)
        self._emailt(email, session['code'])

        return {'ok' : True, 'session_token' : session['token']}

    @required_args(['session_token', 'code', 'name'])
    @check_token()
    def register(self, **args):
        session_token = args['session_token']

        session = self.db.sessions.find_one({'token' : session_token})
        user = self.db.users.find_one({'email' : session['email']})

        if str(session['code']) != args['code']:
            return {'ok' : False, 'description' : 'Incorrect code'}
        elif session['is_authorized']:
            return {'ok' : False, 'description' : 'The session is already authorized'}
        elif user is not None:
            return {'ok' : False, 'description' : 'You are already registered'}
        
        user = {
            '_id' : get_id(self.db, 'users'),
            'email' : session['email'],
            'name' : args['name'],
            'surname' : args.get('surname'),
            'description' : args.get('description'),
            'contacts' : [],
            'groups' : []
        }

        self.db.users.insert_one(user)
        self.db.sessions.update_one(
            {
                'token' : session_token
            },
            {
                '$set' : {
                    'is_authorized' : True,
                    'id_user' : user['_id']
                }
            }
        )

        return {'ok' : True, 'description' : 'Are you registered'}

    @required_args(['session_token', 'code'])
    @check_token()
    def login(self, **args):
        session_token = args['session_token']

        session = self.db.sessions.find_one({'token' : session_token})
        user = self.db.users.find_one({'email' : session['email']})

        if str(session['code']) != args['code']:
            return {'ok' : False, 'description' : 'Incorrect code'}
        elif session['is_authorized']:
            return {'ok' : False, 'description' : 'The session is already authorized'}
        elif user is None:
            return {'ok' : False, 'description' : 'You are not registred'}
        
        self.db.sessions.update(
            {
                'token' : session_token
            },
            {
                '$set' : {
                    'is_authorized' : True,
                    'id_user' : user['_id']
                }
            }
        )

        return {'ok' : True, 'description' : 'You are logged in'}

    @required_args(['session_token'])
    @check_token(is_auth=True)
    def logOut(self, **args):
        self.db.sessions.delete_one({'token' : args['session_token']})

        return {'ok' : True}

        