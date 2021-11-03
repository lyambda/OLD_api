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
    @required_args(['token', 'name'])
    @check_token(is_auth=True)
    def createGroup(self, **args):
        id_user = Session.objects.get(token=args['token']).id_user
        user = User.objects.get(id=id_user)

        group = Group(
            name=args['name'],
            owner=id_user,
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

    @required_args(['token', 'id_group'])
    @check_token(is_auth=True)
    def joinGroup(self, **args):
        if not args['id_group'].isdigit():
            return {'ok' : False, 'error_code' : 400, 'description' : 'Invalid group id'}

        id_user = Session.objects.get(token=args['token']).id_user
        user = User.objects.get(id=id_user)

        try:
            group = Group.objects.get(id=int(args['id_group']))
        except DoesNotExist:
            return {'ok' : False, 'error_code' : 400, 'description' : 'Group not found'}

        if id_user in group.participants:
            return {'ok' : False, 'error_code' : 4030, 'description' : 'You are already in a group'}

        user.groups.append(group.id)
        group.participants.append(id_user)

        user.save()
        group.save()

        return {'ok' : True, 'result' : group.to_mongo().to_dict()}
