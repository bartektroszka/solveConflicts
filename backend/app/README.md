# Backend

To run the backend server run:

### Linux:

```
./run.sh
```

### Windows:

```
commandLine:
pip install -r requirements.txt
$env:FLASK_APP="__init__.py"
$env:FLASK_ENV="development"
'flask run' or 'python -m flask run'
```

### Server is hosted on port 5000

### All the errors will be returned as a single string

### Czasami jest problem z komuniacją ciastkową z Postmanem (trzeba na chwile zakomentować dwie linijki w ```app/__init__.py```)
---

## Following rests are available:

/execute ()

methods: POST

Run the command from backend terminal.
If safe mode is 'True', the command will not be run.

Uwaga, komenty domyślnie wykonywane są w katalogu użytkownika
Można wprowadzić dodatkowe cisateczko, które zapamiętywałoby na przykład
w jakim folderze znajduje się właśnie terminal użytkownika

---

/save_tree

methods: POST

Rest to save the tree that user created on frontend
this rest should have 'nick' and 'tree' values passed

Assumes that the JSON content is formatted correctly
(otherwise it will return an error)

---

/get_tree

methods: GET

Rest to get the size of the tree recursively
There has to be 'path' parameter provided as an argument!

example response:

Poniższy przukłąd zwraca resta, z przykładowym katalogiem usera o hashu c_n8jnaq9z

```JSON
{
    "id": 5,
    "items": [
        {
            "data": "'bbb' \n",
            "id": 6,
            "label": "readme.txt",
            "parentId": 5
        },
        {
            "data": "'aaa' \n",
            "id": 7,
            "label": "readme2.txt",
            "parentId": 5
        }
    ],
    "label": "c_n8jnaq9z",
    "parentId": null
}
```

---
## /get_git_tree [GET]

Rest który zwraca aktualny stan grafu GIT użytkownika

Przykład drzewa dla świeżo zarejestrowanego usera (jest ono po prostu puste):
```JSON
[]
```

Teraz przykład, w którym użytkownik coś pozmieniał (initial commit).

```JSON
[
    {
        "branches": [
            "HEAD -> master"
        ],
        "children": [],
        "hash": "4c93016",
        "parents": []
    }
]
```

Bardziej zaawansowany przykład (z mergem)
```JSON
[
    {
        "branches": [],
        "children": [],
        "hash": "4c93016",
        "parents": [
            "595420b",
            "7a2c1f6"
        ]
    },
    {
        "branches": [
            "branch"
        ],
        "children": [
            "4c93016"
        ],
        "hash": "7a2c1f6",
        "parents": [
            "1ea79d5"
        ]
    },
    {
        "branches": [],
        "children": [
            "4c93016"
        ],
        "hash": "595420b",
        "parents": [
            "1ea79d5"
        ]
    },
    {
        "branches": [
            "HEAD -> master"
        ],
        "children": [
            "595420b",
            "7a2c1f6"
        ],
        "hash": "1ea79d5",
        "parents": []
    }
]
```
---

## /get_my_ip [GET]

Return the ipv4 of a sending entity

--- 

## /index, / [GET, POST]

Empty rest, just to see if backend serwer works