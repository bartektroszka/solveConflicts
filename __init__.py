from flask import Flask, request, send_from_directory
from flask import jsonify
from flask_cors import cross_origin
from .static.check_command import valid_command
import tempfile

app = Flask(__name__)
import json
import os

app.config['SECRET_KEY'] = 'youwillneverfindout'


@app.route("/")
@app.route("/home")
@app.route("/index")
def hello():
    return send_from_directory('templates', 'index.html')


@app.route("/execute", methods=['POST'])
@cross_origin()
def execute():
    content = request.json
    print(content)

    if "command" not in content.keys():
        return jsonify("Musisz podać command jako argument")

    valid = valid_command(content['command'][0])
    return jsonify("KOMENDA JEST POPRAWNA") if valid else jsonify("NIEPOPRAWNA KOMENDA")

    command = request.form['siema']
    print(f'command to run: {command}')
    result_of_command = os.popen(command).read()

    while(command == "hello"):
        pass

    return "<div style='color:red'> " + "Command to run: " + command + "</div>" + \
           "<div style='color:blue'> " + "Result of running the command: " + result_of_command + "</div>"


@app.route("/get_my_ip", methods=["GET"])
def create_directory():
    return jsonify({'ip': request.remote_addr}), 200


@app.route("/random_stuff", methods=['GET'])
def random_stuff():
    return "Hello world!"


if __name__ == '__main__':
    app.run(debug=True)
