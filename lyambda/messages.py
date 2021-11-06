import abc

from .decorators import (
    check_args,
    check_token
)

from .models import (
    Session,
    Message,
    User
)

from mongoengine import (
    DoesNotExist,
    ValidationError
)

from .utils import Utilities

class MessagesMethodsAPI(abc.ABC):
    @check_args(['token', 'chat', 'text'], [], {'token' : str, 'chat' : int, 'text' : str})
    @check_token(is_auth=True)
    def sendMessage(self, token, chat, text):
        user = User.objects.get(id=Session.objects.get(token=token).id_user)
        group = Utilities.get_group(chat, user.id, create_dialog=True)

        if group is None:
            return Utilities.make_reponse(404, 'Chat not found')

        if user.id not in group.participants:
            if group.is_private:
                return Utilities.make_reponse(403, 'Private group')

            return Utilities.make_reponse(403, 'You are not in this group')

        if chat not in user.groups:
            user.groups.append(chat)

        message = Message(
            id_group=group.id,
            from_id=user.id,
            text=text
        )

        try:
            message.save()
            group.save()
            user.save()
        except ValidationError:
            return Utilities.make_reponse(400, 'Invalid parameters')

        return Utilities.make_reponse(200, **{
            'result' : Utilities.filter_message(message.to_mongo().to_dict())
        })

    @check_args(['token', 'chat'], ['offset', 'limit'], {'token' : str, 'chat' : int, 'offset' : int, 'limit' : int})
    @check_token(is_auth=True)
    def getMessages(self, token, chat, offset=0, limit=100):
        id_user = Session.objects.get(token=token).id_user
        group = Utilities.get_group(chat, id_user)

        if group is None:
            return Utilities.make_reponse(404, 'Chat not found')

        if id_user not in group.participants:
            if group.is_private:
                return Utilities.make_reponse(403, 'Private group')

            return Utilities.make_reponse(403, 'You are not in this group')

        messages = list(map(lambda x: Utilities.filter_message(x.to_mongo().to_dict()), Message.objects[offset:offset + limit](id_group=group.id)))
        
        return Utilities.make_reponse(200, **{
            'result' : messages
        })

    @check_args(['token', 'chat', 'id'], [], {'token' : str, 'chat' : int, 'id' : int})
    @check_token(is_auth=True)
    def deleteMessage(self, token, chat, id):
        id_user = Session.objects.get(token=token).id_user
        group = Utilities.get_group(chat, id_user)

        if group is None:
            return Utilities.make_reponse(404, 'Chat not found')

        if id_user not in group.participants:
            if group.is_private:
                return Utilities.make_reponse(403, 'Private group')

            return Utilities.make_reponse(403, 'You are not in this group')

        try:
            message = Message.objects.get(id_group=group.id, from_id=id_user, id=id)
            message.delete()
        except DoesNotExist:
            return Utilities.make_reponse(404, 'Message not found')

        return Utilities.make_reponse(200)
