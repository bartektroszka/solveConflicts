from flask import session
from .utils import user_folder_path, run_command, paths, red
# from .folder_tree import merge_commit_count
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

    if user_path + '\n' == outs:
        return os.path.abspath(os.sep), ""

    return outs[len(user_path):], ""


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
        print("DEBUG: ", command['args'])
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
    session.modified = True

    # z poziomu pythona robimy czyszczenie katalogu użytkownika
    new_path = os.path.abspath(os.path.join('users_data', session['id']))
    assert (os.path.isdir(new_path))
    assert (len(new_path) > 30)  # just to be on the safe side

    run_command(new_path, 'rm -rf * .git/')
    log['git_change'] = log['tree_change'] = True
    return run_command(new_path, os.path.join('..', '..', 'levels', f'level{level}', 'init_level.sh'))


def commands_handler(command, log):
    # TODO wypisz listę komend
    return "nic", "tu", "niema"


def git_add_handler(command, log):  # TODO
    args = command['args']
    if len(args) == 0:
        return "", "Komenda git add przyjmuje przynajmniej jeden argument!"

    if len(command['flagi']) != 0:
        return "", "Nie pozwalamy na podawanie flag do komendy git add!"

    if paths_error := paths(args, kropka=False):
        return "", paths_error

    shell_command = f"git add {' '.join(os.path.abspath(os.path.join(session['cd'], arg)) for arg in args)}"
    return run_command(session['cd'], shell_command)


def git_commit_handler(command, log):
    if len(command['args']) or '-m' not in command['flagi']:
        return "", "Po komendzie git commit należy dodac flagę -m, a poniej wiadomość commita"

    for flaga, lista in command['flagi'].items():
        if flaga != '-m':
            return "", "Dla komendy 'git commit' pozwalamy jedynie na podanie flagi '-m' z jednym argumentem"
        if len(lista) != 1:
            return "", "Flaga -m musi przyjąć dokładnie jeden argument"

    log['git_change'] = True
    return run_command(session['cd'], f"git commit -m {command['flagi']['-m'][0]}")


def git_merge_handler(command, log):
    help_message = "Dla 'git merge' należy podać jeden argument (nazwę gałęzi), a potem dać flagę -m z wiadomością\n" + \
                   "Drugą opcją jest podanie flagi --continue bez żadnego innego arguemntu"

    if len(command['flagi']) == 1 and '--continue' in command['flagi']:
        if len(command['flagi']['--continue']) == 0 and len(command['args']) == 0:
            outs, errs = run_command(session['cd'], 'git merge --continue')
        else:
            return "", help_message
    else:
        if len(command['args']) != 1 or '-m' not in command['flagi']:
            return "", help_message

        for flaga, lista in command['flagi'].items():
            if flaga != '-m':
                return "", help_message
            if len(lista) != 1:
                return "", "Flaga -m musi przyjąć dokładnie jeden argument!"

        outs, errs = run_command(session['cd'], 'git merge ' + command['args'][0] + ' -m ' + command['flagi']['-m'][0])

    log['git_change'] = log['tree_change'] = True
    if 'conflict' in (outs + errs).lower():
        log['conflict'] = True

    return outs, errs


def git_rebase_handler(command, log):
    if len(command['args']) != 1 or '-m' not in command['flagi']:
        return "", "Po komendzie 'git rebase' należy podać jeden argument dodac flagę -m z wiadomością"

    for flaga, lista in command['flagi'].items():
        if flaga != '-m':
            return "", "Dla komendy 'git rebase' pozwalamy jedynie na podanie flagi '-m' z jednym argumentem"
        if len(lista) != 1:
            return "", "Flaga -m musi przyjąć dokładnie jeden argument"

    outs, errs = run_command(session['cd'], 'git rebase ' + command['args'][0] + ' -m ' + command['flagi']['-m'][0])
    log['git_change'] = log['tree_change'] = True

    if 'conflict' in (outs + errs).lower():
        log['conflict'] = True

    return outs, errs


def git_cherry_pick_handler(command, log):
    if len(command['args']) == 0 or '-m' not in command['flagi']:
        return "", "Po komendzie 'git cherry-pick' należy podać przynajmniej jeden argument, dodac potem flagę -m z wiadomością"

    for flaga, lista in command['flagi'].items():
        if flaga != '-m':
            return "", "Dla komendy 'git cherry-pick' pozwalamy jedynie na podanie flagi '-m' z jednym argumentem"
        if len(lista) != 1:
            return "", "Flaga -m musi przyjąć dokładnie jeden argument"

    outs, errs = run_command(session['cd'],
                             'git cherry-pick ' + " ".join(command['args']) + ' -m ' + command['flagi']['-m'][0])
    log['git_change'] = log['tree_change'] = True

    if 'conflict' in (outs + errs).lower():
        log['conflict'] = True

    return outs, errs


def git_log_handler(command, log):
    dozwolone_flagi = ['--graph', '--all', '--oneline', '--decorate']

    for flaga, lista in command['flagi'].items():
        if flaga not in dozwolone_flagi:
            return "", f"Niedozwolona flaga {flaga} (można używać {dozwolone_flagi})"
        if len(lista):
            return "", f"Flaga {flaga} nie może posiadać żadnego argumentu"

    if len(command['args']):
        return "", "Nie pozwalamy na podawanie argumentów 'git log'"

    path = os.path.abspath(os.path.join(session['cd'], command['args'][0])) if command['args'] else ""
    return run_command(session['cd'], f"git log {' '.join(command['flagi'].keys())}")


def git_branch_handler(command, log):
    if len(command['flagi']) != 0:
        return "", "Nie pozwalamy na podawanie flag do komendy 'git branch' [nawet tej od usuwania :( ]!"

    if len(command['args']) > 1:
        return "", "Za dużo argumentów (0 - wypisanie listy gałęzi, 1 - strorzenie nowej gałęzi)"

    return run_command(session['cd'], f"git branch {' '.join(command['args'])}")


def git_status_handler(command, log):
    if len(command['args']) or len(command['flagi']):
        return "", "Nie pozwalamy na podawanie argumentów i flag do komenty 'git status'"

    if len(command['flagi']) != 0:
        return "", "Nie pozwalamy na podawanie flag do komendy ls!"

    return run_command(session['cd'], "git status")


def git_diff_handler(command, log):
    if len(command['flagi']) != 0:
        return "", "Nie pozwalamy na podawanie flag do komendy 'git diff'"

    if len(command['args']) > 1:
        return "", "Za dużo argumentów (0 - poprzedni commit, 1 - jakiś konkretny commit)"

    return run_command(session['cd'], f"git diff {' '.join(command['args'])}")


def git_show_handler(command, log):
    return "TODO", "TODO"


def git_stash_handler(command, log):
    return "TODO", "TODO"


def git_checkout_handler(command, log):
    if len(command['flagi']) != 0:
        return "", "Nie pozwalamy na podawanie flag do komendy 'git diff'"

    if len(command['args']) != 1:
        return "", "Podaj dokładnie jedne argument (nazwę gałęzi)"

    return run_command(session['cd'], f"git checkout {command['args'][0]}")


def hint_handler(command, log):
    if session['level'] == 1:
        if session['stage'] == 1:
            return "Użyj komendy 'git merge friend_branch'", ""
        if session['stage'] == 2:
            return "Pozbądź się konflitku a potem wpisz 'git add przepis.txt' i " \
                   "'git merge --continue -m <wiadomość>' lub 'git commit -m <wiadomość>'", ""
    else:
        log['hint'] = "TODO"

    return "", ""


def list_of_words(command):
    ret = []
    beg = 0
    nawiasek = ""

    for i in range(len(command)):
        letter = command[i]
        if letter in "\"'":
            if nawiasek:
                if letter == nawiasek:  # kończe wystąpienie
                    ret.append(command[beg:i + 1])
                    beg = i + 1
                    nawiasek = ''
            else:
                nawiasek = letter
                ret.extend(command[beg:i].split())
                beg = i

    if nawiasek:
        return ['', nawiasek]

    if beg < len(command):
        ret.extend(command[beg:].split())

    return ret


def parse_command(command):
    words = list_of_words(command)

    print("LISTA WYRAZÓW:", words)

    if len(words) == 2 and words[0] == '':
        return {'command': '', 'args': [words[1]]}  # przepychanie dalej debugu

    start = 1
    base_command = words[0]

    if words[0] == 'git' and len(words) >= 2:
        start = 2
        base_command = " ".join([words[0], words[1]])

    ret = {
        'command': base_command,
        'args': [],
        'flagi': {}
    }

    flag_poz = len(words)

    for i in range(start, len(words)):
        if words[i].startswith('-'):
            ret['args'] = words[start:i]
            flag_poz = i
            break

    if flag_poz == len(words):
        ret['args'] = words[start:]

    for i in range(flag_poz + 1, len(words)):
        if words[i].startswith('-'):  # dodaje nową flagę
            ret['flagi'][words[flag_poz]] = words[flag_poz + 1:i]
            flag_poz = i

    if flag_poz != len(words):
        ret['flagi'][words[flag_poz]] = words[flag_poz + 1:]

    return ret


def handle_command(command, log, sudo=None):  # TODO zamienić sudo na None
    if 'sudo' in session:
        sudo = True

    permission = 1
    if sudo:
        permission = 3

    prohibited = '><&|\\'
    for char in prohibited:
        if char in command:
            command, outs, errs = '-', '', f"Usage of {char} character is prohibited!"

    parsed_command = parse_command(command)
    name = parsed_command['command']

    print(red(f"{parsed_command = }"))
    if len(name) == 0:  # nawias jest niepoprawny
        return "Nawiasy", "", "Jakiś nawias " + parsed_command['args'][0] + " jest bez pary"

    commands_cost = {
        'ls': 1,
        'touch': 1,
        'mkdir': 1,
        'pwd': 1,
        'hint': 1,
        'git log': 1,
        'git status': 1,
        'git diff': 1,
        'git show': 1,
        'show': 1,

        'cd': 2,
        'rm': 2,
        'rmdir': 2,
        'git add': 2,
        'git commit': 2,
        'git rebase': 2,
        'git cherry-pick': 2,
        'git branch': 2,
        'git checkout': 2,
        'git merge': 2,

        'merge_count': 3,
        'init_level': 3
    }

    if name not in commands_cost:
        return "LOV PROVILEGE", "", "Nieprawidłowa komenda. Wpisz komendę 'show', by zobaczyć dozwolone komendy"

    extra_allowed = []

    if session['level'] == 1:
        if session['stage'] == 1:
            extra_allowed.append('git merge')
        if session['stage'] == 2:
            extra_allowed.append('git add')
            extra_allowed.append('git commit')

    if commands_cost[name] <= permission or name in extra_allowed:
        outs, errs = globals()[name.replace(' ', '_').replace('-', '_') + "_handler"](command=parsed_command, log=log)
        return name + " HANDLER", outs, errs
    else:
        return "", "", "Ta komenda jest wyłączona na tym etapie poziomu"
