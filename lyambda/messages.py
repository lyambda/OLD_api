import abc

from .decorators import (
    required_args,
    check_token
)

from .models import (
    Session,
    Group,
    Message
)

from mongoengine import (
    DoesNotExist,
    ValidationError
)

class MessagesMethodsAPI(abc.ABC):
    @required_args(['session_token', 'id_group', 'text'])
    @check_token(is_auth=True)
    def sendMessage(self, **args):
        
        id_user = Session.objects.get(token=args['session_token']).id_user

        try:
            group = Group.objects.get(id=int(args['id_group']))
        except DoesNotExist:
            return {'ok' : False, 'error_code' : 400, 'description' : 'Group not found'}

        if id_user not in group.participants:
            return {'ok' : False, 'error_code' : 403, 'description' : 'You are not in this group'}

        # Нужно сделать нормальную идентификацию сообщений
        message = Message(
            from_id=id_user,
            text=args['text']
        )

        try:
            group.messages.append(message)
            group.save()
        except ValidationError:
            return {'ok' : True, 'error_code' : 400, 'description' : 'Invalid parameters'}

        return {'ok' : True, 'result' : message.to_mongo().to_dict()}

    @required_args(['session_token', 'id_group'])
    @check_token(is_auth=True)
    def getMessages(self, **args):
        id_user = Session.objects.get(token=args['session_token']).id_user

        try:
            group = Group.objects.get(id=int(args['id_group']))
        except DoesNotExist:
            return {'ok' : False, 'error_code' : 400, 'description' : 'Group not found'}

        if id_user not in group.participants:
            return {'ok' : False, 'error_code' : 403, 'description' : 'You are not in this group'}

        return {'ok' : True, 'result' : list(map(lambda x: x.to_mongo().to_dict(), group.messages))}