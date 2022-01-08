from flask import session
from .folder_tree import git_tree
from .utils import user_folder_path
import subprocess

import os


def cd_handler(command, user_id):
    split = command.split()
    assert (split[0] == 'cd')
    if len(split) > 2:
        return "cd command handler", "", "cd can only take one argument!"

    cd, where = split
    new_path = os.path.abspath(os.path.join(session['cd'], where))

    if not os.path.isdir(new_path):
        return "cd command handler", "", "The directory does not exist!"

    if not new_path.startswith(user_folder_path(user_id)):
        return "cd command handler", "", "Trying to escape from root!"

    session['cd'] = new_path
    session.modified = True

    return "cd command handler", "Success!", ""


def rm_handler(command, user_id):
    return "-", "Running rm command!", ""


def show_commands_handler():
    with open('static/all_commands.txt', 'r') as commands_file:
        return "show commands handler", commands_file.read(), ""


def handle_command(command, user_id, cd):
    prohibited = '><|'
    for char in prohibited:
        if char in command:
            command, outs, errs = '-', '', f"Use of {char} character is prohibited!"

    split = command.split()
    if len(command) == 0:
        return "", "", "empty command!?"

    if split[0] == 'cd':
        return cd_handler(command, session['id'])

    elif split[0] == 'rm':
        return rm_handler(command, session['id'])

    elif split[0] == 'show' and split[1] and 'commands':
        return show_commands_handler()

    else:
        command = f"( cd {cd} && {command})"
        print("Running the command: ", command)
        proc = subprocess.Popen(command, text=True, shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        outs, errs = proc.communicate()  # timeout???

        return command, outs, errs
