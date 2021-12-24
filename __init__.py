from flask import Flask, request, jsonify, redirect, make_response, session, Response
from flask_cors import cross_origin
from .static.check_command import valid_command
from .static.folder_tree import recurse_over_tree, get_directory_tree, is_nick, git_tree
from .static.utils import is_nick, random_id, run_command, red, yellow, green
from datetime import timedelta
from flask_cors import CORS

import os

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['SECRET_KEY'] = 'reasumujacwszystkieaspektykwintesencjitematudochodzedofundamentalnejkonkluzjiwartostudiowac'
# Do testowania z postmanem może być konieczne usunięcie dwóch poniższych linijek
# ale gdy postam dostanie już ciastko, można z powrotem od razu przywrócić
app.config['SESSION_COOKIE_SAMESITE'] = "None"
app.config['SESSION_COOKIE_SECURE'] = True


@app.route('/save_tree', methods=['POST'])
def save_tree():
    try:
        register_check()
    except BaseException as exception_message:
        return "[ERROR]" + exception_message

    if not isinstance(request.json, dict):
        return "[ERROR] request.json is not a dictionary"

    if 'tree' not in request.json.keys():
        return "[ERROR] 'tree' key was not specified"

    file_path = os.path.join(os.getcwd(), 'users_data', session['id'])
    return recurse_over_tree(file_path, request.json['tree'])


@app.route("/execute", methods=['POST'])
def execute():
    # TODO This rest it TOTALLY UNSAFE
    allow = True

    try:
        register_check()
    except BaseException as exception_message:
        return exception_message

    if not isinstance(request.json, dict):
        return "[ERROR] json is not a dictionary"

    if 'command' not in request.json.keys():
        return "'command' was not specified"

    command = request.json['command']
    print("Running the command: ", command)

    where = os.path.join(os.getcwd(), 'users_data', session['id'])
    print(f"{where=}")
    stdout = "Command not allowed " if not allow else \
        os.popen(f"( cd {where} && {command} )").read()
    print("DEBUG: ", stdout)

    return jsonify(f"( cd {where} && {command} )", stdout, git_tree(session['id']))


@app.route('/get_tree', methods=['GET'])
def get_tree():
    try:
        register_check()
    except BaseException as exception:
        return exception

    # print(f"{session['id']}")
    path = os.path.join(os.getcwd(), 'users_data', session['id'])
    return jsonify(get_directory_tree(path))


@app.route('/get_my_ip', methods=['GET'])
def get_my_ip():
    return jsonify({'ip': request.remote_addr})


# TODO TA FUNKCJA PEWNIE NIE POWINNA ZNAJDOWAĆ SIĘ W TYM MIEJSCU ALE TRUDNO
def register_check(debug=False):
    if 'id' in session:
        if debug:
            print(f"[INFO] User already has an id: {session['id']}")
    else:
        session['id'] = random_id()
        session.modified = True

    prefix = os.path.join(os.getcwd(), 'users_data')
    if not os.path.isdir(prefix):
        try:  # chyba nie potrzeby o tym informowania
            if debug:
                print("[INFO] Tworzenie katalogu users data")
            os.mkdir(prefix)
        except FileExistsError:
            if debug:
                print("Plik już istnieje (to nie powinno się nigdy wypisać)")
        except:
            raise "Some problem with creating users_data directory"

    path = os.path.join(prefix, session['id'])
    if not os.path.isdir(path):
        if debug:
            print(f"{yellow('[WARNING]')} Missing directory for the user {session['id']}")
        try:
            if debug:
                print(f"{yellow('[WARNING]')} Creating directory for user: {session['id']}")
            os.mkdir(path)
        except FileExistsError:
            if debug:
                print(f"Katalog użytkownika '{path[len(prefix) + 1:]}' już istnieje (Nie powinno się nigdy wypisać)!")
        except:
            raise Exception("Unknown error while creating a directory")

    if debug:
        print(f"Session ID of the user is {session['id']}")


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return "Serwer backendu"


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
