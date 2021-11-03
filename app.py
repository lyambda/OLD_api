from flask import Flask, request, jsonify
from lyambda import API
from config import Config
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

api = API(
    mongodb=Config['mongodb'],
    smtp=Config['smtp']
)

@app.route('/<method>', methods=["GET", "POST"])
def methods(method):
    if method not in api.methods.keys():
        return jsonify({'ok' : False, 'error_code' : 501, 'description' : 'Method not found'})
    else:
        return jsonify(api.methods[method](**request.args.to_dict()))

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'ok' : False, 'error_code' : 500})

if __name__ == '__main__':
    app.run(
        host=Config['server']['host'],
        port=int(os.environ.get('PORT', False)) or Config['server']['port'],
        debug=Config['server']['debug']
    )
