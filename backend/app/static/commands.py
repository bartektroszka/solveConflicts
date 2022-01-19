from flask import session
from .utils import user_folder_path, run_command
from .folder_tree import merge_commit_count
import os


def cd_handler(command):
    split = command.split()
    assert split[0] == 'cd'
    if len(split) > 2 or len(split) == 1:
        return "cd command handler", "", "cd can only take one argument!"

    cd, where = split
    new_path = os.path.abspath(os.path.join(session['cd'], where))

    if not os.path.isdir(new_path):
        return "cd command handler", "", "The directory does not exist!"

    if not new_path.startswith(user_folder_path(session['id'])):
        return "cd command handler", "", "Trying to escape from root!"

    session['cd'] = new_path
    session.modified = True

    return "cd command handler", "Success!", ""


def touch_handler(command, log):
    split = command.split()
    assert split[0] == 'touch'

    if len(split) > 2 or len(split) == 1:
        return "touch command handler", "", "touch can only take one argument!"

    touch, where = split
    new_path = os.path.abspath(os.path.join(session['cd'], where))

    if not new_path.startswith(user_folder_path(session['id'])):
        return "touch command handler", "", "Trying to create file outside of root file!"

    outs, errs = run_command(session['cd'], f"touch {new_path}")
    if len(errs) == 0:
        log['tree_change'] = True

    return "touch command handler", outs, errs


def ls_handler(command):
    split = command.split()
    assert split[0] == 'ls'

    if len(split) > 2:
        return "ls command handler", "", "ls can only take at most one argument!"

    if len(split) == 1:
        outs, errs = run_command(session['cd'], f"ls")
        return "ls command handler", outs, errs

    elif len(split) == 2:
        if split[1] == '-a':
            outs, errs = run_command(session['cd'], f"ls -a")
            return "ls command handler", outs, errs
        else:
            return "ls command handler", "", "Jedyna obsługiwana flaga tego polecenia to '-a'"


def rm_handler(command, log):
    split = command.split()
    assert split[0] == 'rm'

    if len(split) > 2 or len(split) == 1:
        return "rm command handler", "", "rm can only take one argument!"

    rm, where = split
    new_path = os.path.abspath(os.path.join(session['cd'], where))

    if not new_path.startswith(user_folder_path(session['id'])):
        return "rd command handler", "", "Trying to remove some file outside of user sandbox!"

    outs, errs = run_command(session['cd'], f"rm {new_path}")
    if len(errs) == 0:
        log['tree_change'] = True

    return "rm command handler", outs, errs


def rmdir_handler(command, log):
    split = command.split()
    assert split[0] == 'rmdir'

    if len(split) > 2 or len(split) == 1:
        return "rmdir command handler", "", "rmdir can only take one argument!"

    rm, where = split
    new_path = os.path.abspath(os.path.join(session['cd'], where))

    if not new_path.startswith(user_folder_path(session['id'])):
        return "rmdir command handler", "", "Trying to remove some directory outside of user sandbox!"

    outs, errs = run_command(session['cd'], f"rmdir {new_path}")

    if len(errs) == 0:
        log['tree_change'] = True

    return "rmdir command handler", outs, errs


def init_level_handler(command, log=None, sudo=False):
    if not sudo:
        return "init_level command handler", "", "Niedozwolona komenda!"

    split = command.split()
    assert split[0] == 'init_level'

    if len(split) > 2 or len(split) == 1:
        return "init_level command handler", "", "init_level przyjmuje tylko jeden argument (numer poziomu)!"

    _, level = split
    try:
        level = int(level)
    except ValueError:
        return "init_level command handler", "", "init_level niepoprawny argument!"

    if level > 3 or level < 1:
        return "init_level command handler", "", "za duży, albo za mały level!"

    session['folder_ids'] = dict()
    new_path = os.path.abspath(os.path.join('users_data', session['id']))
    # print("SCIEZKA DO SKRYPTU: ", script_path)

    session['level'] = level
    session.modified = True

    outs, errs = run_command(new_path, os.path.join('..', '..', 'levels', f'level{level}', 'init_level.sh'))

    if log is not None:
        log['git_change'] = True
        log['tree_change'] = True

    return "init_level command handler", outs, errs


def show_commands_handler():
    with open('static/all_commands.txt', 'r') as commands_file:
        return "show commands handler", commands_file.read(), ""


def git_add_handler(command):
    # TODO

    outs, errs = run_command(session['cd'], command)
    return command + " (GIT ADD HANDLER)", outs, errs


def git_commit_handler(command, log):
    # TODO
    split = command.split()
    # print(f"DEBUG, {split = }")
    if len(split) < 4 or split[2] != '-m':
        return command + " (GIT COMMIT HANDLER)", "", "Należy podać flagę -m a potem wiadomość do commita"

    outs, errs = run_command(session['cd'], command)
    if len(errs) == 0:  # commit was successful
        log['git_change'] = True

    return command + " (GIT COMMIT HANDLER)", outs, errs


def git_merge_handler(command, log):
    # TODO

    outs, errs = run_command(session['cd'], command)
    if len(errs) == 0:  # commit was successful
        log['git_change'] = True
        log['tree_change'] = True

    if 'CONFLICT' in outs or 'CONFLICT' in errs:
        log['conflict'] = True

    return command + " (GIT MERGE HANDLER)", outs, errs


def git_rebase_handler(command, log):
    # TODO

    outs, errs = run_command(session['cd'], command)
    if len(errs) == 0:  # commit was successful
        log['git_change'] = True
        log['tree_change'] = True

    if 'CONFLICT' in outs or 'CONFLICT' in errs:
        log['conflict'] = True

    return command + " (GIT REBASE HANDLER)", outs, errs


def git_cherry_pick_handler(command, log):
    # TODO

    outs, errs = run_command(session['cd'], command)
    if len(errs) == 0:
        log['git_change'] = True
        log['tree_change'] = True

    if 'CONFLICT' in outs or 'CONFLICT' in errs:
        log['conflict'] = True

    return command + " (GIT CHERRY PICK HANDLER)", outs, errs


def git_log_handler(command):
    # TODO

    outs, errs = run_command(session['cd'], command)
    return command + " (GIT LOG HANDLER)", outs, errs


def git_branch_handler(command):
    # TODO

    outs, errs = run_command(session['cd'], command)
    return command + " (GIT BRANCH HANDLER)", outs, errs


def git_status_handler(command):
    # TODO

    outs, errs = run_command(session['cd'], command)
    return command + " (GIT STATUS HANDLER)", outs, errs


def git_checkout_handler(command):
    # TODO

    outs, errs = run_command(session['cd'], command)
    return command + " (GIT CHECKOUT HANDLER)", outs, errs


def handle_command(command, user_id=None, cd=None, log=None, sudo=None):  # TODO zamienić sudo na None
    if command == 'merge_count':
        return "How many merges have been commited so far", f"{merge_commit_count(user_id) = }", ""

    prohibited = '><&|'
    for char in prohibited:
        if char in command:
            command, outs, errs = '-', '', f"Usage of {char} character is prohibited!"

    split = command.split()
    if len(command) == 0:
        return "", "", "empty command!?"

    if split[0] == 'init_level':
        return init_level_handler(command, log, sudo=sudo)

    if split[0] == 'cd':
        return cd_handler(command)

    elif split[0] == 'rm':
        return rm_handler(command, log)

    elif split[0] == 'touch':
        return touch_handler(command, log)

    elif split[0] == 'ls':
        return ls_handler(command)

    elif split[0] == 'commands':
        return show_commands_handler()

    elif split[0] == 'rmdir':
        return rmdir_handler(command, log)

    elif split[0] == 'git':
        # here we go again...

        if len(split) == 1 or split[1] == 'help':
            return "git help handler", "TODO show git commands", ""

        elif split[1] == 'add':
            return git_add_handler(command)

        elif split[1] == 'commit':
            return git_commit_handler(command, log)

        elif split[1] == 'branch':
            return git_branch_handler(command)

        elif split[1] == 'merge':
            return git_merge_handler(command, log)

        elif split[1] == 'status':
            return git_status_handler(command)

        elif split[1] == 'log':
            return git_log_handler(command)

        elif split[1] == 'checkout':
            return git_checkout_handler(command)

        elif split[1] == 'rebase':
            return git_rebase_handler(command, log)

        elif split[1] == 'cherry-pick':
            return git_cherry_pick_handler(command, log)

        else:
            return "git command handler", "", "UNSUPPORTED GIT COMMAND"

    else:
        # return "", "", "Ta komenda nie jest obsługiwana. Wpisz 'commands', żeby zobaczyć listę dozwolonych komend."
        log['tree_change'] = log['git_change'] = True  # Running custom command - anything can happen
        outs, errs = run_command(cd, command)
        return command + " (KOMENDA OBSŁUGIWANA Z POZIOMU KONSOLI)", outs, errs
