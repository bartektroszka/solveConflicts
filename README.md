# Backend
To run the backend server run:

### Linux:
```
./run.sh
```
###Windows:
```
commandLine:
pip install -r requirements.txt
$env:FLASK_APP="__init__.py"
$env:FLASK_ENV="development"
'flask run' or 'python -m flask run'
```

-----------------------------------------------------------

### Server is hosted on port 5000

### All the errors will be returned as a single string

-----------------------------------------------------------

## Following rests are available:

/execute (safe_mode=True)

methods: POST

Run the command from backend terminal.
If safe mode is 'True', the command will not be run.

___________________________________________________________

/save_tree

methods: POST

Rest to save the tree that user created on frontend
this rest should have 'nick' and 'tree' values passed

Assumes that the JSON content is formatted correctly
(otherwise it will return an error)

-----------------------------------------------------------

/get_tree

methods: GET

Rest to get the size of the tree recursively
There has to be 'path' parameter provided as an argument!

-----------------------------------------------------------

/register

methods: GET

Rest that will correctly set user. It will assign to it a 
unique value, and then create a directory for it. Updated
cookie will be sent in response.

-----------------------------------------------------------

/get_my_ip

methods: "GET"

Return the ipv4 of a sending entity

