from flask import Flask, request, jsonify
from lyambda import API
from config import Config

app = Flask(__name__)
api = API(
    mongodb=Config['mongodb'],
    smtp=Config['smtp']
)

@app.route('/<method>', methods=["GET", "POST"])
def main(method):
    if method not in api.methods.keys():
        return jsonify({'ok' : False, 'description' : 'Method not found'})
    else:
        return jsonify(api.methods[method](**request.args.to_dict()))

if __name__ == '__main__':
    app.run(
        host=Config['server']['host'],
        port=Config['server']['port'],
        debug=True
    )