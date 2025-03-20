import json
import os
from base64 import b64decode

from flask import Flask, request, jsonify, current_app
from werkzeug.security import check_password_hash

from database.select import select_list
from database.sql_provider import SQLProvider

app = Flask(__name__)

with open('data/db_connect.json') as f:
    app.config['db_config'] = json.load(f)

app.config['SECRET_KEY'] = 'Вскормлённый в неволе орёл молодой'

sql_provider = SQLProvider(
    os.path.join(os.path.dirname(__file__), 'sql')
)


def valid_authorization_request(api_request):
    auth_header = api_request.headers.get('Authorization', '')
    if not auth_header:
        return False
    if not auth_header.startswith('Basic '):
        return False
    if len(auth_header) <= len('Basic '):
        return False
    return True


def decode_basic_authorization(api_request):
    auth_header = api_request.headers.get('Authorization')
    encoded_credentials = auth_header.split('Basic ')[1]
    decoded_credentials = b64decode(encoded_credentials).decode('ascii')
    login, password = decoded_credentials.split(':', 1)
    return login, password


@app.route('/find-user')
def find_user():
    if not valid_authorization_request(request):
        return jsonify({'status': 400, 'message': 'Bad request'})
    try:
        login, password = decode_basic_authorization(request)
    except Exception as e:
        return jsonify({'status': 400, 'message': f'Bad request {str(e)}'})
    else:

        sql = sql_provider.get('get_auth_data.sql')
        result, schema = select_list(current_app.config.get('db_config'), sql, (login,))

        if not schema:
            return jsonify({'status': 503, 'message': 'Service Unavailable'})
        if not result:
            return jsonify({'status': 404, 'message': 'user not found'})

        stored_password_hash = result[0][0]
        user_id = result[0][1]
        user_group = result[0][2]

        if not check_password_hash(stored_password_hash, password):
            return jsonify({'status': 401, 'message': 'user password incorrect'})

        return jsonify({'status': 200, 'message': 'OK', 'user_id': user_id, 'user_group': user_group})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002)
