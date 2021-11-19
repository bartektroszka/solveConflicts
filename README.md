to run the server run

Linux:
./run.sh

Windows:
commandLine:
pip install -r requirements.txt
$env:FLASK_APP="__init__.py"
$env:FLASK_ENV="development"
'flask run' or 'python -m flask run'

ip: 127.0.0.1:5000

/execute - rest to communicate with git console (to run the commands in general [for now])

/save_tree - rest to save the tree that user created on frontend
this rest should have 'nick' and 'tree' values passed