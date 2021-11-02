import json
from dotmap import DotMap

with open('config.json', encoding='utf-8') as f:
    Config = json.load(f)