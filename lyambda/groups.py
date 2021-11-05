import abc

from .decorators import (
    required_args,
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

class GroupsMethodsAPI(abc.ABC):
    @required_args(['token', 'name'], types={'token' : str, 'name' : str})
    @check_token(is_auth=True)
    def createGroup(self, **args):
        id_user = Session.objects.get(token=args['token']).id_user
        user = User.objects.get(id=id_user)

        group = Group(
            name=args['name'],
            admins=[id_user],
            link=args.get('username'),
            description=args.get('description'),
            participants=[id_user]
        )

        user.groups.append(group.id)

        try:
            group.save()
            user.save()
        except ValidationError:
            return {'ok' : True, 'error_code' : 400, 'description' : 'Invalid parameters'}

        return {'ok' : True, 'result' : group.to_mongo().to_dict()}

    @required_args(['token', 'id_group'], types={'token' : str, 'id_group' : int})
    @check_token(is_auth=True)
    def joinGroup(self, **args):
        id_user = Session.objects.get(token=args['token']).id_user
        id_group = int(args['id_group'])
        user = User.objects.get(id=id_user)

        try:
            group = Group.objects.get(id=id_group)
        except DoesNotExist:
            return {'ok' : False, 'error_code' : 404, 'description' : 'Group not found'}

        if group.is_private:
            return {'ok' : False, 'error_code' : 403, 'description' : 'Private group'}

        if id_user in group.participants:
            return {'ok' : False, 'error_code' : 403, 'description' : 'You are already in a group'}

        user.groups.append(id_group)
        group.participants.append(id_user)

        user.save()
        group.save()

        return {'ok' : True, 'result' : group.to_mongo().to_dict()}

    @required_args(['token', 'id_group'], types={'token' : str, 'id_group' : int})
    @check_token(is_auth=True)
    def leaveGroup(self, **args):
        id_group = int(args['id_group'])
        id_user = Session.objects.get(token=args['token']).id_user
        user = User.objects.get(id=id_user)

        try:
            group = Group.objects.get(id=id_group)
        except DoesNotExist:
            return {'ok' : False, 'error_code' : 403, 'description' : 'Group not found'}

        if group.is_private:
            return {'ok' : False, 'error_code' : 403, 'description' : 'Private group'}

        if id_user not in group.participants:
            return {'ok' : False, 'error_code' : 400, 'description' : 'You are not in a group'}

        user.groups.remove(id_group)
        group.participants.remove(id_user)

        user.save()
        group.save()

        return {'ok' : True}

    @required_args(['token', 'id_group'], types={'token' : str, 'id_group' : int})
    @check_token(is_auth=True)
    def deleteGroup(self, **args):
        id_group = int(args['id_group'])
        id_user = Session.objects.get(token=args['token']).id_user

        try:
            group = Group.objects.get(id=id_group)
        except DoesNotExist:
            return {'ok' : False, 'error_code' : 403, 'description' : 'Group not found'}

        if group.is_private:
            return {'ok' : False, 'error_code' : 403, 'description' : 'Private group'}

        if id_user not in group.participants:
            return {'ok' : False, 'error_code' : 400, 'description' : 'You are not in a group'}

        if group not in group.admins:
            return {'ok' : False, 'error_code' : 403, 'description' : 'You have no right'}

        group.delete()

        return {'ok' : True}
