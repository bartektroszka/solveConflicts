from flask import Flask, request, send_from_directory
app = Flask(__name__)
import json

app.config['SECRET_KEY'] = 'youwillneverfindout'

@app.route("/")
@app.route("/home")
@app.route("/index")
def hello():
  return send_from_directory('templates', 'index.html')

@app.route("/execute", methods=['POST'])
def execute():
  print(request.form)
  return request.form

if __name__ == '__main__':
  app.run(debug = True)