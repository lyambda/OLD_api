import abc

from .decorators import (
    required_args,
    check_token
)

from .models import (
    Session,
    User
)

class ProfileMethodsAPI(abc.ABC):
    @required_args(['token'])
    @check_token(is_auth=True)
    def me(self, **args):
        id_user = Session.objects.get(token=args['token']).id_user
        user = User.objects.get(id=id_user)
        
        return {'ok' : True, 'result' : user.to_mongo().to_dict()}
