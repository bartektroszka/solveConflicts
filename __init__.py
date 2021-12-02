from flask import Flask, request, jsonify, redirect, make_response, session, Response
from flask_cors import cross_origin
from .static.check_command import valid_command
from .static.folder_tree import recurse_over_tree, get_directory_tree, is_nick
from .static.utils import is_nick, random_id, run_command
from datetime import timedelta
from flask_cors import CORS

import os

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['SECRET_KEY'] = 'reasumujacwszystkieaspektykwintesencjitematudochodzedofundamentalnejkonkluzjiwartostudiowac'

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
    command = request.json
    if not isinstance(command, str):
        return 'Zawartość JSON musi być jednym napisem oznaczającym komendę do wywołania'

    valid = True  # TODO
    print(f'\033[33m[WARNING]\033[m Command to run: {command}')
    print(f'\033[33m[INFO]\033[m {safe_mode = }')

    return 'invalid command' if not valid else '--safe_mode--' if safe_mode else os.popen(command).read()


@app.route('/get_tree', methods=['GET'])
def get_tree():
    if 'id' not in session:
        print(f"\033[33m[WARNING]\033[m User not registered before")
        register()

    prefix = os.path.join(os.getcwd(), 'users_data')
    if not os.path.isdir(prefix):
        return f"[ERROR] there is no users_data folder in application directory"

    path = os.path.join(prefix, session['id'])

    if not os.path.isdir(path):
        print(f"\033[33m[WARNING]\033[m Missing directory for the user {session['id']}")
        try:
            os.mkdir(path)
            print(f"\033[32m[INFO]\033[m Creating a directory for user {path[-10:]}")
        except FileExistsError:
            return f"User '{path[len(prefix) + 1:]}' is already registered!"
        except:
            return "[ERROR] Unknown error while creating a directory"

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
        print(f"\033[32m[INFO]\033[m Creating a directory for user {path[-10:]}")
    except FileExistsError:
        return f"User '{path[len(prefix) + 1:]}' is already registered!"
    except:
        return "[ERROR] Unknown error while creating a directory"

    return f"User id is '{session['id']}'!"


''' TODO
@app.route("/set_level1", methods=["GET"])
def set_level1():
    if 'id' not in session:
        return f"User was not registered!"

    prefix = os.path.join(os.getcwd(), 'users_data')
    if not os.path.isdir(prefix):
        return "[ERROR] No directory called users_data in server directory - unable to create directory for user"

    path = os.path.join(prefix, session['id'])

    print(f"\033[32m[COMMAND TO EXECUTE]\033[m rm -r {os.path.join(path, '*')}")
    run_command(f"( cd {path}; git init )")
    
    run_command(f"( cd {path}; git status )")
    run_command(f"( cd {path}; echo 'some content' > a.txt )")
    run_command(f"( cd {path}; git checkout -b new_branch )")
    run_command(f"( cd {path}; echo 'totally different file contents' > a.txt )")
    run_command(f"( cd {path}; git checkout main )")
    run_command(f"( cd {path}; git merge )")

    return "Created github repository!"
'''

if __name__ == '__main__':
    app.run(debug=True)
