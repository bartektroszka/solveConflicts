import random
import subprocess
from flask import session
import os


def user_folder_path(user_id):
    return os.path.join(os.getcwd(), 'users_data', user_id)


def run_command(where, command):
    command = f"( cd {where} && {command})"
    print("Running the command: ", command)
    proc = subprocess.Popen(command, text=True, shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.communicate()  # timeout???


def is_nick(name):
    alphabet = 'abcdefghijklmnopqrstuvwxyz_0123456789'
    return all([letter in alphabet for letter in name])


def init_repo_for_user(user):
    # print("Initializing repository for user : ", user)
    command = f"git init {os.path.join(os.getcwd(), 'users_data', user)}"
    proc = subprocess.Popen(command, text=True, shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate()  # timeout???


# Functions for managing colors in output console
def red(string_to_color):
    return '\033[31m' + string_to_color + '\033[m'


def yellow(string_to_color):
    return '\033[33m' + string_to_color + '\033[m'


def green(string_to_color):
    return '\033[32m' + string_to_color + '\033[m'


def random_id():
    alphabet = 'abcdefghijklmnopqrstuvwxyz_0123456789'
    return ''.join([random.choice(alphabet) for _ in range(10)])


def register_check(debug=False):
    if 'id' in session:
        if debug:
            print(f"[INFO] User already has an id: {session['id'] =}")
    else:
        session['id'] = random_id()
        session.modified = True

    if 'cd' in session:
        if debug:
            print(f"[INFO] User already has an cd: {session['cd'] = }")
    else:
        session['cd'] = user_folder_path(session['id'])
        session.modified = True

    if 'level' not in session:
        # defaultowo ustawiam poziom usera na 1
        session['level'] = 1
        session.modified = True

    if 'folder_ids' not in session:
        session['folder_ids'] = dict()

    # print("SESSION CD ", session['cd'])
    prefix = os.path.join(os.getcwd(), 'users_data')
    if not os.path.isdir(prefix):
        try:  # chyba nie potrzeby o tym informowania
            if debug:
                print("[INFO] Tworzenie katalogu users data")
            os.mkdir(prefix)
        except FileExistsError:
            if debug:
                print("Plik już istnieje (to nie powinno się nigdy wypisać)")

    path = os.path.join(prefix, session['id'])
    if not os.path.isdir(path):
        if debug:
            print(f"{yellow('[WARNING]')} Missing directory for the user {session['id']}")
        try:
            if debug:
                print(f"{yellow('[WARNING]')} Creating directory for user: {session['id']}")
            os.mkdir(path)
        except FileExistsError:
            if debug:
                print(f"Katalog użytkownika '{path[len(prefix) + 1:]}' już istnieje (Nie powinno się nigdy wypisać)!")

    if not os.path.isdir(os.path.join(path, '.git')):
        print(f"USER {session['id']} DID NOT HAVE REPO PREVIOUSLY!... Initializing reporistory of the user")
        init_repo_for_user(session['id'])

    if debug:
        print(f"Session ID of the user is {session['id']}")
