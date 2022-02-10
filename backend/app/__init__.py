from flask import Flask, request, jsonify, session, send_file
import os
from .static.commands import handle_command, init_level_handler
from .static.folder_tree import recurse_over_tree, get_directory_tree, git_tree
from .static.utils import register_check, green, red, run_command, user_folder_path, app_folder
from flask_cors import CORS
import json

from datetime import date

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['SECRET_KEY'] = 'reasumujacwszystkieaspektykwintesencjitematudochodzedofundamentalnejkonkluzjiwartostudiowac'
# Do testowania z postmanem może być konieczne usunięcie dwóch poniższych linijek
# ale gdy postam dostanie już ciastko, można z powrotem od razu przywrócić
app.config['SESSION_COOKIE_SAMESITE'] = "None"
app.config['SESSION_COOKIE_SECURE'] = True


def start_first_lev_for_new_user(log):
    log['git_change'] = log['tree_change'] = True
    return init_level_handler({"command": "init_level", "args": ["1"], "flags": []}, log)
    # return run_command(user_folder_path(), os.path.join(app_folder(), 'levels', f'level1', 'init_level.sh'))


@app.route('/save_tree', methods=['POST'])
def save_tree():
    ret = {}

    try:
        register_check(log=ret)
    except BaseException as exception_message:
        return jsonify(str(exception_message))

    if 'new_user' in ret:
        # print(green("TRIGGERS INIT_LEVEL AS NEW USER"))
        outs, errs = start_first_lev_for_new_user(ret)
        # print(f"FIRST LEVEL START {outs = } {errs = } {len(git_tree()) = }")

    if not isinstance(request.json, dict):
        return "[ERROR] request.json is not a dictionary"

    if 'tree' not in request.json:
        return "[ERROR] 'tree' key was not specified"

    file_path = os.path.join(app_folder(), 'users_data', session['id'])
    return recurse_over_tree(file_path, request.json['tree'])


@app.route("/execute", methods=['POST', 'GET'])
def execute(command=None, sudo=False):
    # print(f"{session = }")

    ret = {"git_change": False, "tree_change": False, 'admin_info': '', 'stderr': '', 'stdout': ''}

    try:
        register_check(log=ret)
    except BaseException as exception_message:
        ret['stderr'] = ' --- Problem z rejestracją użytwkonika --- '
        ret['admin_info'] = str(exception_message)
        return jsonify(ret)

    if 'new_user' in ret:
        # print(green("TRIGGERS INIT_LEVEL AS NEW USER"))
        outs, errs = start_first_lev_for_new_user(ret)
        # print(f"FIRST LEVEL START {outs = } {errs = } {len(git_tree()) = }")

    # tu były drobne bugi z tym, że nie zawsze mamy obiekt request.json (np dla świeżego usera) i init_level(1)
    if not sudo and not isinstance(request.json, dict):
        ret['stderr'] = ' --- Problem z wewnętrzny aplikacji --- '
        ret['admin_info'] = "Request json, nie jest typu dict()"
        return jsonify(ret)

    if not sudo and 'command' not in request.json.keys():
        ret['stderr'] = ' --- Problem z wewnętrzny aplikacji --- '
        ret['admin_info'] = "Nie podano 'command' ani w request.json ani jako argumentu dla resta"
        return jsonify(ret)

    if isinstance(request.json, dict):
        command = request.json['command'] if 'command' in request.json else command

    admin_info, outs, errs = handle_command(command.strip(),
                                            log=ret,
                                            sudo=sudo)

    # print(green(command))

    ret["admin_info"] = admin_info
    ret["stdout"] = outs  # na wszelki wypadek
    ret["stderr"] = errs
    ret["git_tree"] = git_tree(session['id'])
    ret["level"] = session['level']
    ret["stage"] = session['stage']

    if 'reset' in ret:
        _, outs, errs = handle_command(command=f"init_level {session['level']}",
                                       log=ret,
                                       sudo=True)

        ret['stdout'] += "\n " + ret['reset'] + "\n \n RESETOWANIE POZIOMU"
        ret['tree_change'] = ret['git_change'] = True

    def remove_user_folder(out):
        out = out.replace(user_folder_path() + ' ', os.path.abspath(os.sep))
        out = out.replace(user_folder_path() + '\n', os.path.abspath(os.sep))
        out = out.replace(user_folder_path() + os.sep, os.path.abspath(os.sep))
        out = out.replace(user_folder_path(), os.path.abspath(os.sep))
        return out

    ret['stdout'] = remove_user_folder(ret['stdout'])
    ret['stderr'] = remove_user_folder(ret['stderr'])

    if 'success' in ret:
        if session['level'] not in session['completed']:
            session['completed'].append(session['level'])
            session.modified = True

    ret['completed'] = session['completed']

    print(json.dumps(ret['git_tree'], indent=4))
    return jsonify(ret)


@app.route('/get_tree', methods=['GET'])
def get_tree():
    ret = {}

    try:
        register_check(log=ret)
    except BaseException as exception_message:
        return jsonify(str(exception_message))
    if 'new_user' in ret:
        # print(green("TRIGGERS INIT_LEVEL AS NEW USER"))
        outs, errs = start_first_lev_for_new_user(ret)
        # print(f"FIRST LEVEL START {outs = } {errs = } {len(git_tree()) = }")

    path = os.path.join(app_folder(), 'users_data', session['id'])
    list_of_folders = []
    get_directory_tree(path, list_of_folders)

    ret['tree'] = list_of_folders

    return jsonify(ret)


@app.route("/get_git_tree", methods=['GET'])
def get_git_tree():
    ret = {}

    try:
        register_check(log=ret)
    except BaseException as exception_message:
        return jsonify(str(exception_message))
    if 'new_user' in ret:
        # print(green("TRIGGERS INIT_LEVEL AS NEW USER"))
        outs, errs = start_first_lev_for_new_user(ret)
        # print(f"FIRST LEVEL START {outs = } {errs = } {len(git_tree()) = }")

    ret['git_tree'] = git_tree(session['id'])

    return jsonify(ret)


@app.route('/init_level', methods=['POST'])
def init_level(level=None):
    try:
        register_check()
    except BaseException as exception_message:
        return jsonify(str(exception_message))

    if level is None and 'level' not in request.json.keys():  # TODO -- niby zawsze powinno być request json dict, ale..
        return "", "'level' to init was not specified (for now either 1 or 2)"

    try:
        if level is None:
            level = int(request.json['level'])
    except ValueError:
        return "", "Podany poziom nie jest typem numerycznym!"

    return execute(f"init_level {level}", sudo=True)


@app.route('/get_current_level', methods=['GET'])
def get_current_level():
    ret = {}
    try:
        register_check(log=ret)
    except BaseException as exception_message:
        return jsonify(str(exception_message))

    if 'new_user' in ret:
        # print(green("TRIGGERS INIT_LEVEL AS NEW USER"))
        outs, errs = start_first_lev_for_new_user(ret)
        # print(f"FIRST LEVEL START {outs = } {errs = } {len(git_tree()) = }")

    return jsonify({'level': session['level']})


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return "Serwer backendu"


@app.route('/print', methods=['POST'])
def print_diploma():
    ret = {}
    try:
        register_check(log=ret)
    except BaseException as exception_message:
        return jsonify(str(exception_message))

    if 'new_user' in ret:
        # print(green("TRIGGERS INIT_LEVEL AS NEW USER"))
        outs, errs = start_first_lev_for_new_user(ret)
        # print(f"FIRST LEVEL START {outs = } {errs = } {len(git_tree()) = }")

    assert (isinstance(request.json, dict))
    assert ('name' in request.json)

    name = request.json['name']

    allowed = 'abcdefghijklmnopqrstuvwxyz' + 'abcdefghijklmnopqrstuvwxyz'.upper() + ' ' + 'ĄąĆćĘęŁłŃńÓóŚśŹźŻż'
    for char in name:
        if char not in allowed:
            return jsonify({"error": f"Znak {char} nie jest dopuszczalny w imieniu i nazwisku!"})

    template_file = os.path.join(app_folder(), 'static', 'dyplomy', 'index.html')
    temp_file = os.path.join(app_folder(), 'static', 'dyplomy', 'temp.html')

    if os.path.isfile(temp_file):
        os.remove(temp_file)

    with open(template_file) as inf:
        txt = inf.read()
        txt = txt.replace('user_name', name)
        txt = txt.replace('date', date.today().strftime("%d/%m/%Y"))

        with open(temp_file, 'w') as f2:
            f2.write(txt)

    return send_file(temp_file)
