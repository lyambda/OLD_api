from email.policy import default
from mongoengine import (
    Document,
    SequenceField,
    IntField,
    StringField,
    BooleanField,
    ListField,
    EmailField,
    DateTimeField
)

from mongoengine.connection import get_db
from pymongo import ReturnDocument

import datetime

class MinusSequenceField(SequenceField):
    def generate(self):
        sequence_name = self.get_sequence_name()
        sequence_id = f"{sequence_name}.{self.name}"
        collection = get_db(alias=self.db_alias)[self.collection_name]

        counter = collection.find_one_and_update(
            filter={"_id": sequence_id},
            update={"$inc": {"next": -1}},
            return_document=ReturnDocument.AFTER,
            upsert=True,
        )
        return self.value_decorator(counter["next"])

class Session(Document):
    id = SequenceField(collection_name='ids', sequence_name='sessions', primary_key=True)
    id_user = IntField(min_value=1, null=True)
    email = EmailField(required=True)
    code = IntField(min_value=100000, max_value=999999, required=True)
    token = StringField(min_length=32, max_length=32, unique=True, required=True)
    is_auth = BooleanField(required=True)
    date = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'collection': 'sessions'
    }

class User(Document):
    id = SequenceField(collection_name='ids', sequence_name='users', primary_key=True)
    email = EmailField(required=True)
    name = StringField(required=True, max_length=16)
    surname = StringField(null=True, max_length=16)
    description = StringField(null=True, max_length=64)
    contacts = ListField(IntField(), default=[])
    groups = ListField(IntField(), default=[])

    meta = {
        'collection': 'users'
    }

class Message(Document):
    id = SequenceField(collection_name='ids', sequence_name='messages', primary_key=True)
    id_group = IntField(required=True)
    from_id = IntField(required=True)
    text = StringField(required=True, max_length=2048)
    date = DateTimeField(default=datetime.datetime.utcnow)

class Group(Document):
    id = MinusSequenceField(collection_name='ids', sequence_name='groups', primary_key=True)
    admins = ListField(IntField(), required=True)
    name = StringField(null=True, max_length=16)
    link = StringField(null=True, max_length=16, unique=True)
    description = description = StringField(null=True, max_length=64)
    participants = ListField(IntField(), required=True)
    is_private = BooleanField(default=False)

    meta = {
        'collection': 'groups'
    }