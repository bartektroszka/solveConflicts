from flask import Flask, request, jsonify, redirect, make_response, session, Response
from flask_cors import cross_origin
import os
from .static.check_command import cd_command, rm_command
from .static.folder_tree import recurse_over_tree, get_directory_tree, is_nick, git_tree
from .static.utils import is_nick, random_id, red, yellow, green, register_check
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
    return recurse_over_tree(file_path, request.json['tree'])


@app.route("/execute", methods=['GET'])
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

    command = request.json['command'].strip()

    prohibited = '><|'
    for char in prohibited:
        if char in command:
            command, outs, errs = '-', '', f"Use of {char} character is prohibited!"

    if command.startswith('cd '):
        command, outs, errs = cd_command(command, session['id'])

    elif command.startswith('rm '):
        command, outs, errs = rm_command(command, session['id'])

    else:
        command = f"( cd {session['cd']} && {command})"
        print("Running the command: ", command)
        proc = subprocess.Popen(command, text=True, shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        outs, errs = proc.communicate()  # timeout???

    return jsonify({"command": command, "stdout": outs, "stderr": errs,
                    "git_tree": git_tree(session['id'])})


@app.route('/get_tree', methods=['GET'])
def get_tree():
    try:
        register_check()
    except BaseException as exception_message:
        return jsonify(str(exception_message))

    # print(f"{session['id']}")
    path = os.path.join(os.getcwd(), 'users_data', session['id'])
    return jsonify(get_directory_tree(path))


@app.route('/get_my_ip', methods=['GET'])
def get_my_ip():
    return jsonify({'ip': request.remote_addr})


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return "Serwer backendu"
