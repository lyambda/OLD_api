import abc

from .decorators import (
    check_args,
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
    @check_args(['token'], [], {'token' : str})
    @check_token(is_auth=True)
    def me(self, token):
        user = User.objects.get(id=Session.objects.get(token=token).id_user)
        
        return Utilities.make_reponse(200, **{
            'result' : user.to_mongo().to_dict()
        })

    @check_args(['token'], [], {'token' : str})
    @check_token(is_auth=True)
    def getGroups(self, token):
        user = User.objects.get(id=Session.objects.get(token=token).id_user)
        
        return Utilities.make_reponse(200, **{
            'result' : user.groups
        })

    @check_args(['token', 'id'], [], {'token' : str, 'id' : int})
    @check_token(is_auth=True)
    def getUser(self, token, id):
        id_user = Session.objects.get(token=token).id_user

        try:
            user = User.objects.get(id=id)

            if id_user in user.contacts:
                return Utilities.make_reponse(200, **{
                    'result' : Utilities.filter_user(user.to_mongo().to_dict(), contact=True)
                })

            return Utilities.make_reponse(200, **{
                'result' : Utilities.filter_user(user.to_mongo().to_dict())
            })
        except DoesNotExist:
            return Utilities.make_reponse(404, 'User not found')

    @check_args(['token', 'id'], [], {'token' : str, 'id' : int})
    @check_token(is_auth=True)
    def getChat(self, token, id):
        id_user = Session.objects.get(token=token).id_user

        group = Utilities.get_group(id, id_user)

        if group is None:
            return Utilities.make_reponse(404, 'Chat not found')
 
        if id_user not in group.participants:
            return Utilities.make_reponse(200, **{
                'result' : Utilities.filter_group(group.to_mongo().to_dict())
            })

        return Utilities.make_reponse(200, **{
            'result' : group.to_mongo().to_dict()
        })

    @check_args(['token', 'id'], [], {'token' : str, 'id' : int})
    @check_token(is_auth=True)
    def addContact(self, token, id):
        user = User.objects.get(id=Session.objects.get(token=token).id_user)

        try:
            User.objects.get(id=id)
        except DoesNotExist:
            return Utilities.make_reponse(404, 'User not found')

        if id in user.contacts:
            return Utilities.make_reponse(400, 'Contact has already been added')

        user.contacts.append(id)
        user.save()

        return Utilities.make_reponse(200)

    @check_args(['token', 'id'], [], {'token' : str, 'id' : int})
    @check_token(is_auth=True)
    def deleteContact(self, token, id):
        user = User.objects.get(id=Session.objects.get(token=token).id_user)

        if id not in user.contacts:
            return Utilities.make_reponse(404, 'Contact not found')

        user.contacts.remove(id)
        user.save()

        return Utilities.make_reponse(200)

    @check_args(['token', 'name'], [], {'token' : str, 'name' : str})
    @check_token(is_auth=True)
    def editName(self, token, name):
        if name == '':
            return Utilities.make_reponse(400, 'Invalid parameters')

        user = User.objects.get(id=Session.objects.get(token=token).id_user)
        user.name = name.strip()
        user.save()

        return Utilities.make_reponse(200)

    @check_args(['token', 'surname'], [], {'token' : str, 'surname' : (str, None)})
    @check_token(is_auth=True)
    def editSurname(self, token, surname):
        if surname is not None and not surname.strip():
            return Utilities.make_reponse(400, 'Invalid parameters')

        user = User.objects.get(id=Session.objects.get(token=token).id_user)
        user.surname = surname
        user.save()

        return Utilities.make_reponse(200)

    @check_args(['token', 'description'], [], {'token' : str, 'description' : (str, None)})
    @check_token(is_auth=True)
    def editDescription(self, token, description):
        if description is not None and not description.strip():
            return Utilities.make_reponse(400, 'Invalid parameters')

        user = User.objects.get(id=Session.objects.get(token=token).id_user)
        user.description = description
        user.save()

        return Utilities.make_reponse(200)
