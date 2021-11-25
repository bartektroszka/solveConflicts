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

/get_tree - rest to get the size of the tree recursively
There has to be 'path' parameter provided as an argument!

Usage example: 
sending a rest with argument 'path'
'path':'/home/marcin/siema'

return value:
{
    "filename": "/home/marcin/siema",
    "items": [
        {
            "data": "\nkasfa\nafdsd",
            "filename": "/home/marcin/siema/plik1.txt",
            "parent": "/home/marcin/siema"
        },
        {
            "filename": "/home/marcin/siema/dwa",
            "items": [
                {
                    "data": "",
                    "filename": "/home/marcin/siema/dwa/file3.txt",
                    "parent": "/home/marcin/siema/dwa"
                },
                {
                    "data": "",
                    "filename": "/home/marcin/siema/dwa/file1.txt",
                    "parent": "/home/marcin/siema/dwa"
                },
                {
                    "data": "",
                    "filename": "/home/marcin/siema/dwa/file2.txt",
                    "parent": "/home/marcin/siema/dwa"
                },
                {
                    "data": "",
                    "filename": "/home/marcin/siema/dwa/file4.txt",
                    "parent": "/home/marcin/siema/dwa"
                }
            ],
            "parent": "/home/marcin/siema"
        },
        {
            "data": "problem with reading file data",
            "filename": "/home/marcin/siema/Ja_St1_closer.jpg",
            "parent": "/home/marcin/siema"
        }
    ],
    "parent": null
}
