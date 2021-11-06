import abc

from .decorators import (
    check_args,
    check_token
)

from .models import (
    Session,
    User,
    Group
)

from mongoengine import (
    ValidationError,
    DoesNotExist
)

from .utils import Utilities

class GroupsMethodsAPI(abc.ABC):
    @check_args(['token', 'name'], ['description', 'link'], {'token' : str, 'name' : str, 'description' : str, 'link' : str})
    @check_token(is_auth=True)
    def createGroup(self, token, name,  description=None, link=None):
        id_user = Session.objects.get(token=token).id_user
        user = User.objects.get(id=id_user)

        group = Group(
            name=name,
            admins=[id_user],
            link=link,
            description=description,
            participants=[id_user]
        )

        user.groups.append(group.id)

        try:
            group.save()
            user.save()
        except ValidationError:
            return Utilities.make_reponse(400, 'Invalid parameters')

        return Utilities.make_reponse(200, **{
            'result' : group.to_mongo().to_dict()
        })

    @check_args(['token', 'id_group'], [], {'token' : str, 'id_group' : int})
    @check_token(is_auth=True)
    def joinGroup(self, token, id_group):
        id_user = Session.objects.get(token=token).id_user
        user = User.objects.get(id=id_user)

        try:
            group = Group.objects.get(id=id_group)
        except DoesNotExist:
            return Utilities.make_reponse(404, 'Group not found')

        if group.is_private:
            return Utilities.make_reponse(403, 'Private group')

        if id_user in group.participants:
            return Utilities.make_reponse(403, 'You are already in a group')

        user.groups.append(id_group)
        group.participants.append(id_user)

        user.save()
        group.save()

        return Utilities.make_reponse(200, **{
            'result' : group.to_mongo().to_dict()
        })

    @check_args(['token', 'id_group'], [], {'token' : str, 'id_group' : int})
    @check_token(is_auth=True)
    def leaveGroup(self, token, id_group):
        id_user = Session.objects.get(token=token).id_user
        user = User.objects.get(id=id_user)

        try:
            group = Group.objects.get(id=id_group)
        except DoesNotExist:
            return Utilities.make_reponse(404, 'Group not found')

        if group.is_private:
            return Utilities.make_reponse(403, 'Private group')

        if id_user not in group.participants:
            return Utilities.make_reponse(403, 'You are already in a group')

        user.groups.remove(id_group)
        group.participants.remove(id_user)

        user.save()
        group.save()
        
        return Utilities.make_reponse(200)

    @check_args(['token', 'id_group'], [], {'token' : str, 'id_group' : int})
    @check_token(is_auth=True)
    def deleteGroup(self, token, id_group):
        user = User.objects.get(id=Session.objects.get(token=token).id_user)

        try:
            group = Group.objects.get(id=id_group)
        except DoesNotExist:
            return Utilities.make_reponse(404, 'Group not found')

        if group.is_private:
            return Utilities.make_reponse(403, 'Private group')

        if user.id not in group.participants:
            return Utilities.make_reponse(403, 'You are already in a group')

        if group not in group.admins:
            return Utilities.make_reponse(403, 'You have no right')

        user.groups.remove(group.id)
        
        group.delete()
        user.save()

        return Utilities.make_reponse(200)
