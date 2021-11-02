from . import (
    BaseMethodsAPI,
    ProfileMethodsAPI
)

import pymongo
import inspect

class API(BaseMethodsAPI, ProfileMethodsAPI):
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.methods = {i[0] : i[1] for i in inspect.getmembers(instance, predicate=inspect.ismethod) if not i[0].startswith('_')}

        return instance

    def __init__(self, mongodb, smtp):
        self.client = pymongo.MongoClient(
            host=mongodb['host'],
            port=mongodb['port'],
        )

        self.db = self.client[mongodb['database']]
        self.smtp = smtp