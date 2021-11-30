from flask import Flask, request, jsonify, redirect, make_response, session, Response
from flask_cors import cross_origin
from .static.check_command import valid_command
from .static.folder_tree import recurse_over_tree, get_directory_tree, is_nick
from .static.utils import is_nick, random_id
from datetime import timedelta
from flask_cors import CORS

import os

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['SECRET_KEY'] = 'reasumujacwszystkieaspektykwintesencjitematudochodzedofundamentalnejkonkluzjiwartostudiowac'
#app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
app.config['SESSION_COOKIE_SAMESITE'] = "None"
app.config['SESSION_COOKIE_SECURE'] = True


@app.route('/save_tree', methods=['POST'])
def save_tree():
    if 'id' not in session:
        return "[ERROR] User has not generated an id"

    if not isinstance(request.json, dict):
        return "[ERROR] request.json is not a dictionary"

    if 'tree' not in request.json.keys():
        return "[ERROR] 'tree' key was not specified"

    file_path = os.path.abspath(os.getcwd())
    file_path = os.path.join(file_path, 'users_data')

    if not os.path.isdir(file_path):
        return "[ERROR] no 'users_data' directory in application directory"

    file_path = os.path.join(file_path, session['id'])

    if not os.path.isdir(file_path):
        return f"[ERROR] No user folder for id '{session['id']}'"

    return recurse_over_tree(file_path, request.json['tree'])


@app.route('/execute', methods=['POST'])
def execute(safe_mode=True):
    content = request.json
    print(content)

    if 'command' not in content.keys():
        return jsonify('Musisz podać command jako argument')

    command = content['command'][0]
    valid = valid_command(command)
    print(jsonify('This command begins with "git" word') if valid else jsonify('Incorrect git command'))

    print(f'command to run: {command}')
    result_of_command = 'invalid command' if not valid else 'safe mode' if safe_mode else os.popen(command).read()
    return jsonify(result_of_command)


@app.route('/get_tree', methods=['GET'])
def get_tree():
    if 'id' not in session:
        register()

    prefix = os.path.join(os.getcwd(), 'users_data')
    if not os.path.isdir(prefix):
        return f"[ERROR] there is no users_data folder in application directory"

    path = os.path.join(prefix, session['id'])
    if not os.path.isdir(path):
        return f"[ERROR] there is no user called {session['id']}"

    return jsonify(get_directory_tree(path, len(prefix) + 1))


@app.route('/get_my_ip', methods=['GET'])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200


@app.route('/register', methods=['GET'])
def register():
    if 'id' in session:
        return f"User already has an id: {session['id']}"
    session['id'] = random_id()
    session.modified = True

    prefix = os.path.join(os.getcwd(), 'users_data')
    if not os.path.isdir(prefix):
        return "[ERROR] No directory called users_data in server directory - unable to create directory for user"

    path = os.path.join(prefix, session['id'])

    try:
        os.mkdir(path)
        print(f"\033[32m[INFO]\033[m Creating a directory {path} for now user")
    except FileExistsError:
        return f"User '{path[len(prefix) + 1:]}' is already registered!"
    except:
        return "[ERROR] Unknown error while creating a directory"

    return f"User id is '{session['id']}'!"


if __name__ == '__main__':
    app.run(debug=True)
