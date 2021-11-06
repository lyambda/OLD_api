from flask import Flask, request, Response, abort
from config import Config
from lyambda import API
from lyambda.utils import Utilities
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

api = API(
    mongodb=Config['mongodb'],
    smtp=Config['smtp']
)

@app.route('/<method>', methods=['POST'])
def methods(method):
    data = request.get_json()

    if data is None:
        abort(400)
    elif method not in api.methods.keys():
        abort(404)
    else:
        return Response(*api.methods[method](**data), {'Content-Type': 'application/json'})

@app.errorhandler(400)
def bad_request(e):
    return Response(*Utilities.make_reponse(400, 'Bad request'), {'Content-Type': 'application/json'})

@app.errorhandler(404)
def not_found(e):
    return Response(*Utilities.make_reponse(404, 'Method not found'), {'Content-Type': 'application/json'})

@app.errorhandler(405)
def method_not_allowed(e):
    return Response(*Utilities.make_reponse(405, 'Method Not Allowed'), {'Content-Type': 'application/json'})

@app.errorhandler(500)
def internal_server_error(e):
    return Response(*Utilities.make_reponse(500, 'Internal server error'), {'Content-Type': 'application/json'})
    
if __name__ == '__main__':
    app.run(
        host=Config['server']['host'],
        port=int(os.environ.get('PORT', False)) or Config['server']['port'],
        debug=Config['server']['debug']
    )
