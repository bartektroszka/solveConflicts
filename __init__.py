from flask import Flask, request, jsonify, session
import os
from .static.commands import handle_command
from .static.folder_tree import recurse_over_tree, get_directory_tree, git_tree, merge_commit_count
from .static.utils import register_check
from .static.levels import check_success
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['SECRET_KEY'] = 'reasumujacwszystkieaspektykwintesencjitematudochodzedofundamentalnejkonkluzjiwartostudiowac'
# Do testowania z postmanem może być konieczne usunięcie dwóch poniższych linijek
# ale gdy postam dostanie już ciastko, można z powrotem od razu przywrócić
app.config['SESSION_COOKIE_SAMESITE'] = "None"
app.config['SESSION_COOKIE_SECURE'] = True


@app.route('/save_tree', methods=['POST'])
def save_tree():
    ret = {}

    try:
        register_check(log=ret)
    except BaseException as exception_message:
        return jsonify(str(exception_message))

    if not isinstance(request.json, dict):
        return "[ERROR] request.json is not a dictionary"

    if 'tree' not in request.json.keys():
        return "[ERROR] 'tree' key was not specified"

    file_path = os.path.join(os.getcwd(), 'users_data', session['id'])
    # print("DEBUG: ", request.json['tree'])
    if 'new_user' in ret:
        init_level(session['level'])

    return recurse_over_tree(file_path, request.json['tree'])


@app.route("/get_git_tree", methods=['GET'])
def get_git_tree():
    ret = {}

    try:
        register_check(log=ret)
    except BaseException as exception_message:
        return jsonify(str(exception_message))

    ret['git_tree'] = git_tree(session['id'])
    if 'new_user' in ret:
        init_level(session['level'])

    return jsonify(ret)


@app.route("/execute", methods=['POST'])
def execute(command=None, sudo=True):
    print("GIT EXECUTE")
    log = {"git_change": False, "tree_change": False}

    try:
        register_check(log=log)
    except BaseException as exception_message:
        return jsonify(str(exception_message))

    # print(f"{session['id'] = }")
    if not isinstance(request.json, dict):
        return "[ERROR] json is not a dictionary"

    if 'command' not in request.json.keys() and command is None:
        return "'command' was not specified"

    command = request.json['command'] if 'command' in request.json else command

    num_of_merges_then = merge_commit_count(session['id'])
    command, outs, errs = handle_command(command.strip(),
                                         user_id=session['id'],
                                         cd=session['cd'],
                                         log=log,
                                         sudo=sudo)
    num_of_merges_now = merge_commit_count(session['id'])
    merged = num_of_merges_then < num_of_merges_now

    ret = {
        "command": command,
        "stdout": outs,
        "stderr": errs,
        "git_tree": git_tree(session['id']),
        "git_change": log['git_change'],
        "tree_change": log["tree_change"],
        "level": session['level'],
        "merged": merged
    }

    if 'new_user' in log:
        ret['new_user'] = True

    if 'conflict' in log:
        ret['conflict'] = True

    check_success(ret)

    if 'reset' in ret:
        init_level(ret["level"])

    if 'new_user' in ret:
        init_level(session['level'])

    return jsonify(ret)


@app.route('/get_current_level', methods=['GET'])
def get_current_level():
    ret = {}

    try:
        register_check(log=ret)
    except BaseException as exception_message:
        return jsonify(str(exception_message))

    ret['level'] = session['level']

    if 'new_user' in ret:
        init_level(session['level'])

    return jsonify(ret)


@app.route('/get_tree', methods=['GET'])
def get_tree():
    ret = {}

    try:
        register_check(log=ret)
    except BaseException as exception_message:
        return jsonify(str(exception_message))

    path = os.path.join(os.getcwd(), 'users_data', session['id'])
    list_of_folders = []
    get_directory_tree(path, list_of_folders)

    ret['tree'] = list_of_folders
    if 'new_user' in ret:
        init_level(session['level'])

    return jsonify(ret)


@app.route('/init_level', methods=['POST'])
def init_level(level=None):
    print("INIT LEVEL:")
    try:
        register_check()
    except BaseException as exception_message:
        return jsonify(str(exception_message))

    if level is None and 'level' not in request.json.keys():  # TODO -- niby zawsze powinno być request json dict, ale..
        return "'level' to init was not specified (for now either 1 or 2)"

    try:
        if level is None:
            level = int(request.json['level'])
    except ValueError:
        return "Podany poziom nie jest typem numerycznym!"
    ret = execute(f"init_level {level}", sudo=True)
    print("FINISHED INITING LEVEL:", level)
    return ret


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return "Serwer backendu"
