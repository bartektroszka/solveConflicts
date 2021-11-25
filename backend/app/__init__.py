from flask import Flask, request, send_from_directory
from flask import jsonify
from flask_cors import cross_origin
from .static.check_command import valid_command
from .static.folder_tree import list_of_commands_to_update_tree, get_directory_tree
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
    my_dict = {
        'nick': 'marcin',
        'tree': []
    }

    content = request.json
    # assert (isinstance(content, dict))

    return jsonify(list_of_commands_to_update_tree(content))


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


@app.route('/get_tree', methods=['POST'])
def get_tree():
    print("ARGUMENTS", request.args)

    if 'path' not in request.args.keys():
        return jsonify("Pass path as a part of request!")

    return jsonify(get_directory_tree(request.args['path']))


@app.route('/get_my_ip', methods=['GET'])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200


if __name__ == '__main__':
    app.run(debug=True)
