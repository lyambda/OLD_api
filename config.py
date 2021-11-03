import json
import os

with open(os.path.join(os.path.dirname(__file__), 'config.json'), encoding='utf-8') as f:
    Config = json.load(f)