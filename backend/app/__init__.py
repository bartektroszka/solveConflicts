from flask import Flask, request, jsonify, redirect, make_response, session, Response
from flask_cors import cross_origin
import os
from .static.commands import handle_command
from .static.folder_tree import recurse_over_tree, get_directory_tree, git_tree
from .static.utils import random_id, red, yellow, green, register_check, run_command
from datetime import timedelta
from flask_cors import CORS
import subprocess

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
        return jsonify(str(exception_message))

    if not isinstance(request.json, dict):
        return "[ERROR] request.json is not a dictionary"

    if 'tree' not in request.json.keys():
        return "[ERROR] 'tree' key was not specified"

    file_path = os.path.join(os.getcwd(), 'users_data', session['id'])
    print("DEBUG: ", request.json['tree'])
    return recurse_over_tree(file_path, request.json['tree'])


@app.route("/get_git_tree", methods=['GET'])
def get_git_tree():
    try:
        register_check()
    except BaseException as exception_message:
        return jsonify(str(exception_message))

    return jsonify(git_tree(session['id']))


@app.route("/execute", methods=['POST'])
def execute():
    try:
        register_check()
    except BaseException as exception_message:
        return jsonify(str(exception_message))

    print(f"{session['id'] = }")
    if not isinstance(request.json, dict):
        return "[ERROR] json is not a dictionary"

    if 'command' not in request.json.keys():
        return "'command' was not specified"

    log = {"git_change": False, "tree_change": False, 'merge': False}
    command, outs, errs = handle_command(request.json['command'].strip(), user_id=session['id'], cd=session['cd'],
                                         log=log)

    return {"command": command, "stdout": outs, "stderr": errs, "git_tree": git_tree(session['id']),
            "git_change": log['git_change'], "tree_change": log["tree_change"], "merge": log["merge"], 'success': log["merge"]}


@app.route('/get_tree', methods=['GET'])
def get_tree():
    try:
        register_check()
    except BaseException as exception_message:
        return jsonify(str(exception_message))

    # print(f"{session['id']}")
    path = os.path.join(os.getcwd(), 'users_data', session['id'])
    list_of_folders = []
    get_directory_tree(path, list_of_folders)

    return jsonify(list_of_folders);


@app.route('/init_first_level', methods=['GET'])
def init_first_level():
    try:
        register_check()
    except BaseException as exception_message:
        return jsonify(str(exception_message))

    path = os.path.join(os.getcwd(), 'users_data', session['id'])

    run_command(path, '../../levels/level1/init_level.sh')

    return "level initialized"


@app.route('/get_my_ip', methods=['GET'])
def get_my_ip():
    return jsonify({'ip': request.remote_addr})


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return "Serwer backendu"

