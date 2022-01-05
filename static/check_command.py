from flask import session
import os


def user_folder_path(user_id):
    print(f"{user_id=} ZWRACAM {os.path.join(os.getcwd(), 'users_data', user_id) = }")
    return os.path.join(os.getcwd(), 'users_data', user_id)


def cd_command(command, user_id):
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


def rm_command(command, user_id):
    return "-", "Running rm command!", ""
