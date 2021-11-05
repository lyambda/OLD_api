import random
import string

from .models import (
    Session,
    Group,
    User
)

from mongoengine import (
    DoesNotExist
)

from mongoengine.queryset.visitor import Q

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
import smtplib
import os

class Utilities:
    @staticmethod
    def emailt(email, code, smtp):
        env = Environment(loader=FileSystemLoader('%s/html/' % os.path.dirname(__file__)))
        template = env.get_template('new.html')
        output = template.render(data={'code' : code, 'mail' : email})

        message = MIMEMultipart()

        message['From'] = smtp['email']
        message['To'] = email
        message['Subject'] = "Lamda"

        message.attach(MIMEText(output, 'html'))

        server = smtplib.SMTP(f'{smtp["host"]}: {smtp["port"]}')
        server.starttls()
        server.login(smtp['email'], smtp['password'])
        server.sendmail(message['From'], message['To'], message.as_string())
        server.quit()

    @staticmethod
    def delete_not_auth_sesion(email):
        try:
            session = Session.objects.get(email=email, is_auth=False)
            session.delete()
        except DoesNotExist:
            pass

    @staticmethod
    def generate_token():
        return ''.join(random.sample(string.ascii_letters + string.digits, 32))

    @staticmethod
    def get_group(chat, id_user, create_dialog=False):
        try:
            if id_user == chat:
                return Group.objects.get(participants=[id_user], is_private=True)
            else:
                user2 = User.objects.get(id=chat)

                try:
                    return Group.objects.get(participants__all=[id_user, user2.id])
                except DoesNotExist:
                    if not create_dialog:
                        return None

                    return Group(
                        admins=[id_user, user2.id],
                        participants=[id_user, user2.id],
                        is_private=True
                    )
        except DoesNotExist:
            try:
                return Group.objects.get(id=chat)
            except DoesNotExist:
                return None
    
    @staticmethod
    def filter_message(message):
        return {i : j for i, j in message.items() if i != 'id_group'}

    @staticmethod
    def filter_user(user, contact=False):
        filters = ['contacts', 'groups', 'email']

        if contact:
            filters.remove('email')

        return {i : j for i, j in user.items() if i not in filters}

    @staticmethod
    def filter_group(user):
        return {i : j for i, j in user.items() if i not in ['admins', 'participants']}

    def is_int(string):
        try:
            int(string)
            return True
        except ValueError:
            return False