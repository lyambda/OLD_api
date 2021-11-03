import random
import string

def generate_token():
    return ''.join(random.sample(string.ascii_letters + string.digits, 32))

def get_id(db, name):
    collection = db.ids

    if collection.find_one({'_id': name}) is None:
        document = {
            '_id': name,
            'value' : 1
        }

        collection.insert_one(document)
    else:
        document = collection.find_and_modify(
            query={'_id': name},
            update={'$inc' : {'value' : 1}},
            new=True
        )

    return document['value']

