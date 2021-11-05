from flask import Flask, request, jsonify, abort
from lyambda import API
from config import Config
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

api = API(
    mongodb=Config['mongodb'],
    smtp=Config['smtp']
)

@app.route('/<method>', methods=['POST'])
def methods(method):
    if method not in api.methods.keys():
        abort(404)
    else:
        data, code =  api.methods[method](**request.form.to_dict())

    return jsonify(data), code, {'Content-Type': 'application/json'}

@app.errorhandler(404)
def not_found(e):
    return jsonify({'ok' : False, 'error_code' : 404, 'description' : 'Method not found'}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'ok' : False, 'error_code' : 405, 'description' : 'Method Not Allowed'}), 405

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'ok' : False, 'error_code' : 500, 'description' : 'Internal server error'}), 500, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run(
        host=Config['server']['host'],
        port=int(os.environ.get('PORT', False)) or Config['server']['port'],
        debug=Config['server']['debug']
    )
