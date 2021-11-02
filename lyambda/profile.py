import abc

from .utils import (
    get_id
)

from .decorators import (
    required_args,
    check_token
)

import datetime

class ProfileMethodsAPI(abc.ABC):
    @required_args(['session_token'])
    @check_token(is_auth=True)
    def me(self, **args):
        id_user = self.db.sessions.find_one({'token' : args['session_token']})['id_user']
        user = self.db.users.find_one({'_id' : id_user})

        return {'ok' : True, 'result' : user}

    @required_args(['session_token', 'name'])
    @check_token(is_auth=True)
    def createGroup(self, **args):
        id_user = self.db.sessions.find_one({'token' : args['session_token']})['id_user']

        group = {
            '_id' : get_id(self.db, 'groups'),
            'name' : args['name'],
            'username' : args.get('username'),
            'description' : args.get('description'),
            'messages' : [],
            'participants' : [id_user]
        }

        self.db.groups.insert_one(group)
        self.db.users.update_one(
            {
                '_id' : id_user
            },
            {
                '$push' : {'groups' : group['_id']}
            }
        )

        return {'ok' : True, 'result' : group}

    @required_args(['session_token', 'id_group'])
    @check_token(is_auth=True)
    def joinGroup(self, **args):
        if not args['id_group'].isdigit():
            return {'ok' : False, 'description' : 'Invalid group id'}

        id_user = self.db.sessions.find_one({'token' : args['session_token']})['id_user']
        group = self.db.groups.find_one({'_id' : int(args['id_group'])})

        if group is None:
            return {'ok' : False, 'description' : 'Group not found'}

        if id_user not in group['participants']:
            return {'ok' : False, 'description' : 'You are not in this group'}

        self.db.users.update_one(
            {
                '_id' : id_user
            },
            {
                '$push' : {'groups' : group['_id']}
            }
        )

        self.db.groups.update_one(
            {
                '_id' : group['_id']
            },
            {
                '$push' : {'participants' : id_user}
            }
        )

        return {'ok' : True, 'result' : self.db.groups.find_one({'_id' : int(args['id_group'])})}

    @required_args(['session_token', 'id_group', 'text'])
    @check_token(is_auth=True)
    def sendMessage(self, **args):
        if not args['id_group'].isdigit():
            return {'ok' : False, 'description' : 'Invalid group id'}

        id_user = self.db.sessions.find_one({'token' : args['session_token']})['id_user']
        group = self.db.groups.find_one({'_id' : int(args['id_group'])})

        if group is None:
            return {'ok' : False, 'description' : 'Group not found'}

        if id_user not in group['participants']:
            return {'ok' : False, 'description' : 'You are not in this group'}

        message = {
            'id' : get_id(self.db, 'group_' + args['id_group']),
            'from_id' : id_user,
            'text' : args['text'],
            'date' : datetime.datetime.today()
        }

        self.db.groups.update(
            {
                '_id' : group['_id']
            },
            {
                '$push' : {'messages' : message}
            }
        )

        return {'ok' : True, 'result' : message}

    @required_args(['session_token', 'id_group'])
    @check_token(is_auth=True)
    def getMessages(self, **args):
        if not args['id_group'].isdigit():
            return {'ok' : False, 'description' : 'Invalid group id'}

        id_user = self.db.sessions.find_one({'token' : args['session_token']})['id_user']
        group = self.db.groups.find_one({'_id' : int(args['id_group'])})

        if group is None:
            return {'ok' : False, 'description' : 'Group not found'}

        if id_user not in group['participants']:
            return {'ok' : False, 'description' : 'You are not in this group'}

        return {'ok' : True, 'result' : group['messages']}