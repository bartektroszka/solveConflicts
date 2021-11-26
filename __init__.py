from flask import Flask, request, send_from_directory
from flask import jsonify
from flask_cors import cross_origin
from .static.check_command import valid_command
from .static.folder_tree import update_tree, get_directory_tree, is_nick
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'reasumujacwszystkieaspektykwintesencjitematudochodzedofundamentalnejkonkluzjiwartostudiowac'


@app.route('/')
@app.route('/home')
@app.route('/index')
def hello():
    return send_from_directory('templates', 'index.html')


@app.route('/save_tree', methods=['POST'])
@cross_origin()
def save_tree():
    return jsonify(update_tree(request.json))


@app.route('/execute', methods=['POST'])
@cross_origin()
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


@app.route('/log_user', methods=["POST"])
@cross_origin()
def log_user():
    content = request.json
    if not isinstance(content, dict):
        return "request.json is not a directory!"

    if 'nick' not in content.keys():
        return "'nick' value was not specified"
    if not is_nick(content['nick']):
        return "'nick' value must consist only of digits and low latin letter"

    prefix = os.path.join(os.getcwd(), 'users_data')
    try:
        assert (os.path.isdir(prefix))
    except AssertionError:
        return "[internal error] No directory users_data in server directory"

    path = os.path.join(prefix, content['nick'])

    try:
        os.mkdir(path)
    except FileExistsError:
        return f"User '{path[len(prefix) + 1:]}' is already registered!"
    except:
        return "Unknown error"

    return f"Successfully registered user '{path[len(prefix) + 1:]}'!"


@app.route('/get_tree', methods=['POST'])
@cross_origin()
def get_tree():
    content = request.json
    if 'nick' not in content.keys():
        return ["'nick' value was not specified"]
    if not is_nick(content['nick']):
        return ["'nick' value must consist only of digits and low latin letter"]

    prefix = os.path.join(os.getcwd(), 'users_data')

    try:
        assert (os.path.isdir(prefix))
    except AssertionError:
        return ["No directory users_data in server directory"]

    path = os.path.join(prefix, content['nick'])

    if not os.path.isdir(path):
        return [f"there is no user called {content['nick']}"]

    return jsonify(get_directory_tree(path, len(prefix) + 1))


@app.route('/get_my_ip', methods=['GET'])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200


if __name__ == '__main__':
    app.run(debug=True)
