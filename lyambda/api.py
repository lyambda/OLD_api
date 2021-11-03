from . import (
    BaseMethodsAPI,
    ProfileMethodsAPI,
    GroupsMethodsAPI,
    MessagesMethodsAPI
)

from mongoengine import connect
import inspect

class API(BaseMethodsAPI, ProfileMethodsAPI, GroupsMethodsAPI, MessagesMethodsAPI):
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.methods = {i[0] : i[1] for i in inspect.getmembers(instance, predicate=inspect.ismethod) if not i[0].startswith('_')}

        return instance

    def __init__(self, mongodb, smtp):
        connect(host=mongodb)

        self.smtp = smtp