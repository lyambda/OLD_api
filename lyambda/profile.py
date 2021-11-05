import abc

from .decorators import (
    required_args,
    check_token
)

from .models import (
    Session,
    User
)

from mongoengine import (
    DoesNotExist
)

from .utils import Utilities

class ProfileMethodsAPI(abc.ABC):
    @required_args(['token'], types={'token' : str})
    @check_token(is_auth=True)
    def me(self, **args):
        user = User.objects.get(id=Session.objects.get(token=args['token']).id_user)
        
        return {'ok' : True, 'result' : user.to_mongo().to_dict()}

    @required_args(['token'], types={'token' : str})
    @check_token(is_auth=True)
    def getGroups(self, **args):
        user = User.objects.get(id=Session.objects.get(token=args['token']).id_user)
        
        return {'ok' : True, 'result' : user.groups}

    @required_args(['token', 'id'], types={'token' : str, 'id' : int})
    @check_token(is_auth=True)
    def getUser(self, **args):
        id_user = Session.objects.get(token=args['token']).id_user
        id = int(args['id'])

        try:
            user = User.objects.get(id=id)

            if id_user in user.contacts:
                return {'ok' : True, 'result' : Utilities.filter_user(user.to_mongo().to_dict(), contact=True)}

            return {'ok' : True, 'result' : Utilities.filter_user(user.to_mongo().to_dict())}
        except DoesNotExist:
            return {'ok' : False, 'error_code' : 404, 'description' : 'User not found'}

    @required_args(['token', 'id'], types={'token' : str, 'id' : int})
    @check_token(is_auth=True)
    def getChat(self, **args):
        id_user = Session.objects.get(token=args['token']).id_user
        chat = int(args['id'])

        group = Utilities.get_group(chat, id_user)

        if group is None:
            return {'ok' : False, 'error_code' : 404, 'description' : 'Chat not found'}

        if id_user not in group.participants:
            return {'ok' : True, 'result' : Utilities.filter_group(group.to_mongo().to_dict())}

        return {'ok' : True, 'result' : group.to_mongo().to_dict()}

    @required_args(['token', 'id'], types={'token' : str, 'id' : int})
    @check_token(is_auth=True)
    def addContact(self, **args):
        user = User.objects.get(id=Session.objects.get(token=args['token']).id_user)
        id = int(args['id'])

        try:
            User.objects.get(id=id)
        except DoesNotExist:
            return {'ok' : False, 'error_code' : 404, 'description' : 'User not found'}

        if id in user.contacts:
            return {'ok' : False, 'error_code' : 400, 'description' : 'Contact has already been added'}

        user.contacts.append(id)
        user.save()

        return {'ok' : True}

    @required_args(['token', 'id'], types={'token' : str, 'id' : int})
    @check_token(is_auth=True)
    def deleteContact(self, **args):
        user = User.objects.get(id=Session.objects.get(token=args['token']).id_user)
        id = int(args['id'])

        if id not in user.contacts:
            return {'ok' : False, 'error_code' : 404, 'description' : 'Contact not found'}

        user.contacts.remove(id)
        user.save()

        return {'ok' : True}

    @required_args(['token', 'name'], types={'token' : str, 'name' : str})
    @check_token(is_auth=True)
    def editName(self, **args):
        if args['name'] == '':
            return {'ok' : False, 'error_code' : 400, 'description' : 'Invalid parameters'}

        user = User.objects.get(id=Session.objects.get(token=args['token']).id_user)
        user.name = args['name'].strip()
        user.save()

        return {'ok' : True}

    @required_args(['token', 'surname'], types={'token' : str, 'surname' : str})
    @check_token(is_auth=True)
    def editSurname(self, **args):
        user = User.objects.get(id=Session.objects.get(token=args['token']).id_user)
        user.surname = None if not args['surname'] else args['surname'].strip()
        user.save()

        return {'ok' : True}

    @required_args(['token', 'description'], types={'token' : str, 'description' : str})
    @check_token(is_auth=True)
    def editDescription(self, **args):
        user = User.objects.get(id=Session.objects.get(token=args['token']).id_user)
        user.description = None if not args['description'] else args['description'].strip()
        user.save()

        return {'ok' : True}
