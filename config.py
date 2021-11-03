import json
import os

with open(os.path.join(os.path.dirname(__file__), 'config.json'), encoding='utf-8') as f:
    Config = json.load(f)

is_heroku = os.environ.get('HEROKU', False)

if is_heroku:
    Config['server']['host'] = '0.0.0.0'
    Config['server']['port'] = int(os.environ.get('PORT', 5000))