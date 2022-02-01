from flask import session
from .utils import paths, run_command, user_folder_path
import os


def cd_handler(command, log):
    # TODO TEST
    if len(command['args']) != 1:
        return "", "Komenda cd ma przyjąć dokładnie jeden argument"

    if paths_error := paths(command['args']):
        return "", paths_error

    session.modified = True
    err_message = ''
    try:
        # TODO TEST
        new_path = os.path.join(session['cd'], command['args'][0])
        assert os.path.isdir(new_path)
        session['cd'] = os.path.abspath(new_path)
        session.modified = True

    except AssertionError:
        err_message = "Nie ma takiego katalogu"

    return "", err_message


def touch_handler(command, log):
    name = command['command']
    args = command['args']
    if len(args) == 0:
        return "", f"Komenda {name} przyjmuje przynajmniej jeden argument!"

    if len(command['flagi']) != 0:
        return "", f"Nie pozwalamy na podawanie flag do komendy {name}!"

    if paths_error := paths(args):
        return "", paths_error

    log['tree_change'] = True
    return run_command(session['cd'],
                       f"{name} {' '.join(os.path.abspath(os.path.join(session['cd'], arg)) for arg in args)}")


def mkdir_handler(command, log):  # this is basically the same as for touch handler
    return touch_handler(command, log)


def ls_handler(command, log):
    # TODO flagi
    args = command['args']
    if len(args) > 1:
        return "", "Komenda ls może przyjąć jeden lub zero argumentów"

    if len(command['flagi']) != 0:
        return "", "Nie pozwalamy na podawanie flag do komendy ls!"

    if paths_error := paths(args):
        return "", paths_error

    path = os.path.abspath(os.path.join(session['cd'], args[0])) if len(args) else ""
    return run_command(session['cd'], f"ls {path}")


def pwd_handler(command, log):
    if len(command['flagi']) != 0 or len(command['args']):
        return "", "Nie pozwalamy na podawanie flag do komendy pwd!"

    outs, errs = run_command(session['cd'], f"pwd")
    if errs:
        return "", "ERROR: " + errs
    assert errs == ''

    user_path = user_folder_path()
    assert outs.startswith(user_path)

    return outs, errs


def rm_handler(command, log):
    args = command['args']
    if len(args) == 0:
        return "", "Komenda rm przyjmuje przynajmniej jeden argument!"

    if len(command['flagi']) != 0:
        return "", "Nie pozwalamy na podawanie flag do komendy rm!"

    # for flaga, lista in command['flagi'].items():
    #     if flaga != '-r':
    #         return "niepoprawna flaga", "", "Dla komendy 'rm' pozwalamy jedynie na podanie flagi '-r'"
    #     command['args'].extend(lista)

    if paths_error := paths(args):
        return "", paths_error

    log['tree_change'] = True
    flaga = '-r ' if '-r' in command['flagi'] else ''

    shell_command = f"rm {flaga}{' '.join(os.path.abspath(os.path.join(session['cd'], arg)) for arg in args)}"
    return run_command(session['cd'], shell_command)


def rmdir_handler(command, log):
    args = command['args']
    if len(args) == 0:
        return "", "Komenda rmdir przyjmuje przynajmniej jeden argument!"

    if len(command['flagi']) != 0:
        return "", "Nie pozwalamy na podawanie flag do komendy rmdir!"

    if paths_error := paths(args):
        return "", paths_error

    log['tree_change'] = True
    shell_command = f"rmdir {' '.join(os.path.abspath(os.path.join(session['cd'], arg)) for arg in args)}"
    return run_command(session['cd'], shell_command)


def init_level_handler(command, log):
    if len(command['args']) != 1:
        return "", "init_level przyjmuje tylko jeden argument (numer poziomu)!"

    try:
        level = int(command['args'][0])
    except ValueError:
        return "", "Numer poziomu musi być liczbą całkowit z przedziału [1,5]"

    if not (1 <= level <= 5):
        return "", "za duży, albo za mały level!"

    session['folder_ids'] = dict()
    session['level'] = level
    session['stage'] = 1
    log['tree_change'] = log['git_change'] = True
    session.modified = True

    # z poziomu pythona robimy czyszczenie katalogu użytkownika
    new_path = os.path.abspath(os.path.join('users_data', session['id']))
    assert (os.path.isdir(new_path))
    assert (len(new_path) > 30)  # just to be on the safe side

    run_command(new_path, 'rm -rf * .git/')
    log['git_change'] = log['tree_change'] = True

    return run_command(new_path, os.path.join('..', '..', 'levels', f'level{level}', 'init_level.sh'))


def show_level_handler(command=None, log=None):
    return str(session['level']), ":" + str(session['stage'])
