import random
import string

def generate_token():
    return ''.join(random.sample(string.ascii_letters + string.digits, 32))


