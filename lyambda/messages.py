import abc

from .decorators import (
    required_args,
    check_token
)

from .models import (
    Session,
    Message,
)

from mongoengine import (
    DoesNotExist,
    ValidationError
)

from .utils import Utilities

class MessagesMethodsAPI(abc.ABC):
    @required_args(['token', 'chat', 'text'], types={'token' : str, 'chat' : int, 'text' : str})
    @check_token(is_auth=True)
    def sendMessage(self, **args):
        chat = int(args['chat'])
        id_user = Session.objects.get(token=args['token']).id_user
        group = Utilities.get_group(chat, id_user, create_dialog=True)

        if group is None:
            return {'ok' : False, 'error_code' : 404, 'description' : 'Chat not found'}

        if id_user not in group.participants:
            if group.is_private:
                return {'ok' : False, 'error_code' : 403, 'description' : 'Private group'}

            return {'ok' : False, 'error_code' : 403, 'description' : 'You are not in this group'}

        message = Message(
            id_group=group.id,
            from_id=id_user,
            text=args['text']
        )

        try:
            message.save()
            group.save()
        except ValidationError:
            return {'ok' : True, 'error_code' : 400, 'description' : 'Invalid parameters'}

        return {'ok' : True, 'result' : Utilities.filter_message(message.to_mongo().to_dict())}

    @required_args(['token', 'chat'], types={'token' : str, 'chat' : int})
    @check_token(is_auth=True)
    def getMessages(self, **args):
        chat = int(args['chat'])
        offset = args.get('offset', '0')
        limit = args.get('limit', '100')
        id_user = Session.objects.get(token=args['token']).id_user
        group = Utilities.get_group(chat, id_user)

        if group is None:
            return {'ok' : False, 'error_code' : 404, 'description' : 'Chat not found'}

        if not Utilities.is_int(offset) or not Utilities.is_int(limit):
            return {'ok' : False, 'error_code' : 400, 'description' : 'Invalid parameters'}

        if id_user not in group.participants:
            if group.is_private:
                return {'ok' : False, 'error_code' : 403, 'description' : 'Private group'}

            return {'ok' : False, 'error_code' : 403, 'description' : 'You are not in this group'}

        messages = list(map(lambda x: Utilities.filter_message(x.to_mongo().to_dict()), Message.objects[int(offset):int(offset) + int(limit)](id_group=group.id)))

        return {'ok' : True, 'result' : messages}

    @required_args(['token', 'chat', 'id'], types={'token' : str, 'chat' : int, 'id' : int})
    @check_token(is_auth=True)
    def deleteMessage(self, **args):
        chat = int(args['chat'])
        id = int(args['id'])
        id_user = Session.objects.get(token=args['token']).id_user
        group = Utilities.get_group(chat, id_user)

        if group is None:
            return {'ok' : False, 'error_code' : 404, 'description' : 'Chat not found'}

        if id_user not in group.participants:
            if group.is_private:
                return {'ok' : False, 'error_code' : 403, 'description' : 'Private group'}

            return {'ok' : False, 'error_code' : 403, 'description' : 'You are not in this group'}

        try:
            message = Message.objects.get(id_group=group.id, from_id=id_user, id=id)
            message.delete()
        except DoesNotExist:
            return {'ok' : False, 'error_code' : 404, 'description' : 'Message not found'}

        return {'ok' : True}
