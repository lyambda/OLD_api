from email.policy import default
from mongoengine import (
    Document,
    EmbeddedDocument,
    SequenceField,
    IntField,
    StringField,
    BooleanField,
    ListField,
    EmailField,
    EmbeddedDocumentListField,
    DateTimeField
)

import datetime

class Session(Document):
    id = SequenceField(collection_name='ids', sequence_name='sessions', primary_key=True)
    id_user = IntField(min_value=1, null=True)
    email = EmailField(required=True)
    code = IntField(min_value=100000, max_value=999999, required=True)
    token = StringField(min_length=32, max_length=32, required=True)
    is_authorized = BooleanField(required=True)

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

class Message(EmbeddedDocument):
    id = SequenceField(collection_name='ids', sequence_name='messages', primary_key=True)
    from_id = IntField(required=True)
    text = StringField(required=True, max_length=2048)
    date = DateTimeField(default=datetime.datetime.utcnow)

class Group(Document):
    id = SequenceField(collection_name='ids', sequence_name='groups', primary_key=True)
    owner = IntField(required=True)
    name = StringField(required=True, max_length=16)
    link = StringField(null=True, max_length=16)
    description = description = StringField(null=True, max_length=64)
    messages = EmbeddedDocumentListField(Message)
    participants = ListField(IntField(), default=[], required=True)

    meta = {
        'collection': 'groups'
    }