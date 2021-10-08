from flask import Flask, request, send_from_directory
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
def execute():
  command = request.form['siema']
  print(f'command to run: {command}')
  result_of_command = os.popen(command).read()

  return "<div style='color:red'> " + "Command to run: " + command + "</div>" +\
         "<div style='color:blue'> " + "Result of running the command: " + result_of_command + "</div>"

@app.route("/random_stuff", methods = ['GET'])
def random_stuff():
  return "Hello world!"

if __name__ == '__main__':
  app.run(debug = True)