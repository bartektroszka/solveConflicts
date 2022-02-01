import random
import subprocess
from flask import session
import os
import json


def user_folder_path(user_id=None):
    if user_id is None:
        user_id = session['id']

    return os.path.join(os.getcwd(), 'users_data', user_id)


def run_command(where, command):
    command = f"( cd {where} && {command})"
    # print(red(command))
    proc = subprocess.Popen(command,
                            text=True,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    return proc.communicate()  # timeout???


def is_nick(name):
    alphabet = 'abcdefghijklmnopqrstuvwxyz_0123456789'
    return all([letter in alphabet for letter in name])


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


def register_check(log=None, debug=False):
    if 'id' not in session:
        log['new_user'] = True
        session['id'] = random_id()
        session.modified = True

    if 'completed' not in session:
        session['completed'] = {}
        session.modified = True

    if 'cd' not in session or not os.path.isdir(session['cd']):
        session['cd'] = user_folder_path(session['id'])
        session.modified = True

    if 'level' not in session:
        # defaultowo ustawiam poziom usera na 1
        session['level'] = 1

    if 'stage' not in session:
        session['stage'] = 1
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
            if log is not None:
                log['new_user'] = True
            if debug:
                print(f"{yellow('[WARNING]')} Creating directory for user: {session['id']}")
            os.mkdir(path)

        except FileExistsError:
            if debug:
                print(f"Katalog użytkownika '{path[len(prefix) + 1:]}' już istnieje (Nie powinno się nigdy wypisać)!")

    if not os.path.isdir(os.path.join(path, '.git')):
        run_command(path, "git init")

    if debug:
        print(f"Session ID of the user is {session['id']}")


def paths(args, kropka=False):
    for arg in args:
        if arg.startswith('.') and kropka:  # TODO fix jeżeli nie chcemy ukrytych plików
            return "Któryś z plików zaczyna się od '.'"

        new_path = os.path.abspath(os.path.join(session['cd'], arg))

        if not new_path.startswith(user_folder_path(session['id'])):
            return "Próba ucieczki z roota :("
    return ""


def import_expected_git_tree(level):
    with open(os.path.join('levels', f'level{level}', 'expected_git_tree.json')) as f:
        return json.load(f)


def no_spaces(string):
    return string.replace(" ", "").replace("\t", "").replace("\n", "")
