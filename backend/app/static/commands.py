# Moduł zawirający nasze próby przechwycenia komend użytkownika
# W celu pozwolenia tylko na te, które nie zaszkodzą aplikacji

from .utils import import_expected_git_tree, red, green, raw_run, user_folder_path, run_command, app_folder
from .folder_tree import git_tree
from .levels import check_success, check_stage, add_extra_allowed, hint_handler
import os
from flask import session

# Słownik który dla każdej dostępnej komendy określa jakie trzeba mieć uprawnienia do korzystania z niej
commands_cost = {
    'hint': 1,
    'reset': 1,
    'help': 1,

    'ls': 1,
    'touch': 1,
    'mkdir': 1,
    'pwd': 1,
    'git log': 1,
    'git status': 1,
    'git diff': 1,
    'git restore': 1,

    'cd': 2,
    'rm': 2,
    'rmdir': 2,
    'git add': 2,
    # ZREZYGNOWALIŚMY Z GIT STASH, BO JEGO UŻYCIE ZAWSZE POWODOWAŁO ZMIANĘ KSZTAŁTU DRZEWA GIT (CZYLI KONIEC POZIOMU)
    # 'git stash': 2,
    'git commit': 2,
    'git rebase': 2,
    'git cherry-pick': 2,
    'git branch': 2,
    'git checkout': 2,
    'git merge': 2,

    'init_level': 3, # Te opcje nie powinny być dostępne tylko dla aministratorów
    'show_level': 3
}

# Słownik przypisujący każdej komendzie jej krótką techniczą specyfikację
short_help_messages = {
    'hint': "hint",
    'reset': 'reset',
    'help': "help *COMMAND",

    'ls': "ls [DIR]",
    'touch': "touch +FILE",
    'mkdir': "mkdir +DIR",
    'pwd': "pwd",
    'git log': "git log [--graph] [--all] [--oneline] [--decorate] [--reflog]",
    'git status': "git status",
    'git diff': "git diff [COMMIT] [COMMIT] [--cached]",
    'git restore': 'git restore +FILE',

    'cd': "cd <DIR>",
    'rm': "rm +FILE",
    'rmdir': "rmdir +DIR",
    'git add': "git add +DIR/FILE\ngit add <-A>",
    # 'git stash': "git stash <COMMAND> [ARG]",
    'git commit': "git commit [-m MESSAGE]",
    'git rebase': "git rebase <BRANCH/COMMIT> [-X theirs/ours]\ngit rebase --continue\ngit rebase --abort",
    'git cherry-pick': "git cherry-pick +COMMIT [-X theirs/ours]\ngit cherry-pick --continue\ngit cherry-pick --abort",
    'git branch': "git branch\ngit branch [-d/-D BRANCH]",
    'git checkout': "git checkout [-b] <BRANCH>",
    'git merge': "git merge <BRANCH> [-m MESSAGE] [-X theirs/ours]\ngit merge --continue\ngit merge --abort",

    'init_level': "init_level <INT> // ADMIN COMMAND",
    'show_level': "show_level // ADMIN COMMAND"
}

# Słownik przypisujący każdej komendzie jej opisową specyfikację
long_help_messages = {
    'hint': "hint -- Nakierowanie na rozwiązanie poziomu",
    'reset': "reset -- Zresetuj aktualny poziom",
    'help': "help -- Pokaż aktualnie dostępne komendy. Zbiór komend może się zmieniać pomiędzy " +
            "poziomami, a nawet pomiędzy poszczególnymi etapami poziomów. Jako argument można podać " +
            "konkretne komendy, by uzyskać o nich bardziej szczegółowe informacje.",

    'ls': "ls -- Wypisz zawartości katalogu",
    'touch': "touch -- Stwórz nowy plik",
    'mkdir': "mkdir -- Stwórz nowy katalog katalogów",
    'pwd': "pwd -- Wypisz pełną ścieżkę aktualnego katalogu",
    'git log': "git log -- Wypisz aktualny stan grafu repozytorium (historii zmian)",
    'git status': "git status -- Sprawdź status repozytorium",
    'git diff': "git diff -- Podaj różnicę między 'staging tree' oraz 'working tree'. "
                "Flaga --cached sprawia, że będziemy porównywać stan 'staging tree' z repozytorium po ostatnim komicie."
                "Podając argument w formie hasza podajemy z jakim commitem chcemy porównać aktualne HEAD. "
                "Podając dwa argumenty porównamy ze sobą dwa konkrente commity (choć mogą to być też gałęzie)",
    'git restore': "git restore -- Odzyskaj stanu plików sprzed zmian",

    'cd': "cd -- Zmień aktualny katalog",
    'rm': "rm -- Usuń plik",
    'rmdir': "rmdir -- Usuń katalog",
    'git add': "git add -- Dodaj pliki do 'staging area' w celu późniejszego ich scommitowania",
    # 'git stash': "gti stash -- Wyczyść stan 'working tree' zachowując w osobnym miejscu."
    #              "Git stash, przyjmuje jeden lub dwa argumenty. Pierwszy może być jednym z pięciu poleceń "
    #              "[save, pop, drop, clear, apply]. Jeżeli jest to save, drop, lub apply, to należy podać drugi."
    #               "argument.",
    'git commit': "git commit -- Zapisz zmiany w drzewie repozytorium (tworzy nowy commit - wierzchołek w grafie)"
                  "Flaga -m pozwala na dodanie wiadomości do commita",
    'git merge': "git merge -- Połącz dwie gałęzie. Flaga -m służy do podania wiadomości. "
                 "Flaga -X podaje Gitowi, jakiej strategii powinien używać przy rozwiazywaniu konfliktu.\n"
                 "Opcja --continue kontunuuje rozpoczęty wcześniej merge.\n" +
                 "Opcja --abort porzuca proces merge",
    'git rebase': "git rebase -- Podepnij gałąź do innego miejsca w drzewie. Opcjonalna flaga -X przyjmuje "
                  "Flaga -X podaje Gitowi, jakiej strategii powinien używać przy rozwiazywaniu konfliktu.\n"
                  "Opcja --continue kontunuuje rozpoczęty wcześniej rebase.\n" +
                  "Opcja --abort porzuca proces rebase",

    'git cherry-pick': "git cherry-pick -- wyłuskaj odpowiednie commity do swojej gałęzi." +
                       "Podobnie jak przy merge i rebase mamy dostęp do flag --continue, --abort oraz -X",
    'git branch': "git branch -- Pokaż listę gałęzi. Flaga -d pozwala na usunięcie jakiejś gałęzi",
    'git checkout': "git checkout -- przejdź na inną gałąź (flaga -b tworzy nową gałąź)",

    'init_level': "init_level -- Wymuś rozpoczęcie jakiegoś poziomu",
    'show_level': "show_level -- Pokaż aktualny poziom i stage"
}

# ---------------------------------------------------------------------------------------+
# Poniżej znajdują sie implementacje handlerów komend obsługiwanych przez naszą aplikację|
# ---------------------------------------------------------------------------------------+


def full_help_message(command_name):
    return short_help_messages[command_name] + '\n' + long_help_messages[command_name] + '\n\n'


def no_parentheses(string):
    if string[0] == string[-1] and string[0] in "'\"":
        string = string[1:-1]
    return string


def paths(args, files=False, dirs=False):
    for arg in args:
        sufix = no_parentheses(arg)
        new_path = os.path.abspath(os.path.join(session['cd'], sufix))

        if not new_path.startswith(user_folder_path(session['id'])):
            return f"Próba ucieczki z katalogu domowego dla ścieżki '{sufix}'"

        is_file = os.path.isfile(new_path)
        is_dir = os.path.isdir(new_path)

        if files and not dirs:
            if not is_file:
                return f"Ścieżka {sufix} nie prowadzi do pliku"

        if dirs and not files:
            if not is_dir:
                return f"Ścieżka {sufix} nie prowadzi do katalogu"

        if dirs and files:
            if not is_dir and not is_file:
                return f"Ścieżka {sufix} nie prowadzi ani do pliku ani do katalogu"

    return ""


def check_command_flags(command, template):
    if 'flags' not in template:
        template['flags'] = {}

    def check_num_of_args(ile, args):
        if ile == '*':
            pass
        elif ile == '+':
            if len(args) == 0:
                return "Należy podać chociaż jeden argument"
        else:
            # ile jest listą dozwolonych długości listy argumentów
            if len(args) not in ile:
                return f"{len(args)} to niedozwolona liczba argumentów"

        return ""

    if args_error := check_num_of_args(template['num_args'], command['args']):
        return args_error + " dla komendy " + command['command']

    if 'is_path' in template:
        p = template['is_path']
        if paths_error := paths(command['args'], files=p['files'], dirs=p['dirs']):
            return paths_error

    for flag in command['flags']:
        if flag not in template['flags']:
            return f"Flaga {flag} nie jest dozwolona dla komendy " + command['command']

    for flag in command['flags']:
        if args_error := check_num_of_args(template['flags'][flag], command['flags'][flag]):
            return args_error + " dla flagi " + flag

    return ""


def format_flags(command):
    return " ".join([f'{flag} {" ".join(args)}' for flag, args in command['flags'].items()])


def format_command(command):
    return f"{command['command']} {' '.join(command['args'])} {format_flags(command)}"


def finish_command(command, template, log):
    if err := check_command_flags(command, template):
        return "", err

    if 'on_success' in template:
        for flag in template['on_success']:
            log[flag] = True

    return run_command(session['cd'], format_command(command))


def help_handler(command, log):
    allowed = log['allowed']

    outs = '<> - obowiązkowe pole\n[] - opcjonalne pole\n+ jedno lub więcej pól\n* zero lub więcej pól\n\n'
    if len(command['args']) == 0:
        # wypisujemy wszystkie dostępne na tym poziomie komendy (w skrócie)
        for command_name in allowed:
            outs += short_help_messages[command_name] + '\n'

        outs += "\nWięcej informacji po podaniu konkretnej komendy np:\nhelp \"git diff\" rmdir"

    else:
        for flag, flag_args in command['flags'].items():
            return "", f"Komenda 'help' nie oczekuje flags {flag}"

        command['args'] = [no_parentheses(com) for com in command['args']]

        for command_name in command['args']:
            if command_name not in commands_cost:
                return "", f"Niepoprawna komenda {command_name}"

        for command_name in command['args']:
            if command_name not in allowed:
                return "", f"Komenda {command_name} nie jest dostępna na tym etapie poziomu"

        for command_name in command['args']:
            outs += full_help_message(command_name)

    return outs, ""


def cd_handler(command, log):
    template = {
        'num_args': [1],
        'is_path': {'files': False, 'dirs': True},
    }

    if err := check_command_flags(command, template):
        return "", err

    new_path = os.path.join(session['cd'], command['args'][0])
    assert os.path.isdir(new_path)

    session['cd'] = os.path.abspath(new_path)
    session.modified = True

    return "", ""


def touch_handler(command, log):
    template = {
        'num_args': '+',
        'is_path': {'files': False, 'dirs': False},  # to wciąż sprawdzi, czy user nie chce wyjść z roota
        'on_success': ['tree_change']
    }
    return finish_command(command, template, log)


def mkdir_handler(command, log):  # Z grubsza robimy tu takie same sprawdzenia jak dla touch
    return touch_handler(command, log)


def ls_handler(command, log):
    template = {
        'num_args': [0, 1],
        'is_path': {'files': False, 'dirs': True}
    }
    return finish_command(command, template, log)


def pwd_handler(command, log):
    template = {
        'num_args': [0],
    }
    return finish_command(command, template, log)


def rm_handler(command, log):
    template = {
        'num_args': [0],
        'is_path': {'files': True, 'dirs': True},
        'flags': {'-r': '*'},
        'on_success': ['tree_change']
    }
    return finish_command(command, template, log)


def rmdir_handler(command, log):
    template = {
        'num_args': [0],
        'is_path': {'files': False, 'dirs': True},
        'on_success': ['tree_change']
    }
    return finish_command(command, template, log)


def init_level_handler(command, log):
    if len(command['args']) != 1:
        return "", "init_level przyjmuje tylko jeden argument (numer poziomu)!"

    try:
        level = int(command['args'][0])
    except ValueError:
        return "", "Numer poziomu musi być liczbą całkowitą z przedziału [1,8]"

    if not (1 <= level <= 8):
        return "", "za duży, albo za mały level!"

    session['folder_ids'] = dict()
    session['level'] = level
    session['stage'] = 1
    log['tree_change'] = log['git_change'] = True
    session.modified = True

    new_path = user_folder_path(session['id'])
    assert (os.path.isdir(new_path))

    run_command(new_path, 'rm -rf * .git/')
    log['git_change'] = log['tree_change'] = True

    return run_command(new_path, os.path.join(app_folder(), 'levels', f'level{level}', 'init_level.sh'))


def reset_handler(command, log):
    if len(command['args']) or len(command['flags']):
        return "", "'reset' nie przyjmuje żadnych argumentów, ani flag"

    log['reload'] = True
    command['args'] = [session['level']]
    return init_level_handler(command, log)  # zakładamy, że to wywołanie będzie zawsze prawidłowe


def show_level_handler(command=None, log=None):
    return str(session['level']), ":" + str(session['stage'])


# ---------------------------------------------------------------------------------------+
# Zostały jeszcze komendy gitowe                                                         |
# ---------------------------------------------------------------------------------------+


def git_restore_handler(command, log):
    template = {
        'num_args': '+',
        'is_path': {'files': True, 'dirs': True},
        'on_success': ['tree_change', 'git_change']
    }
    return finish_command(command, template, log)

'''
def git_stash_handler(command, log):
    help_message = "Git stash, przyjmuje jeden lub dwa argumenty. Pierwszy argument moze być jednym z pięciu poleceń " \
                   "[save, pop, drop, clear, apply]. Jeżeli jest to save, drop, lub apply, to należy podać drugi." \
                   "argument."

    if len(command['flags']) != 0:
        return "", "Nie pozwalamy na podawanie żadnych flag do komendy git stash!"

    args = command['args']
    if len(args) == 0 or len(args) > 2:
        return "", help_message

    jeden = ['pop', 'clear']
    dwa = ['save', 'drop', 'apply']

    if (len(args) == 1 and args[0] not in jeden) or (len(args) == 2 and args[0] not in dwa):
        return "", help_message

    log['tree_change'] = log['git_change'] = True
    shell_command = f"git stash {args[0]} {args[1] if len(args) == 2 else ''}"
    return run_command(session['cd'], shell_command)
'''


def git_add_handler(command, log):
    template = {
        'num_args': '+',
        'flags': {'-A': [0], '--all': [0]},
        'is_path': {'files': True, 'dirs': True}
    }
    return finish_command(command, template, log)


def git_commit_handler(command, log):
    template = {
        'num_args': [0],
        'flags': {'-m': [1]},
        'on_success': ['git_change']
    }
    return finish_command(command, template, log)


def git_merge_handler(command, log):
    template = {
        'on_success': ['git_change', 'tree_change']
    }

    if '--continue' in command['flags']:
        template['num_args'] = [0]
        template['flags'] = {"--continue": [0]}

    elif '--abort' in command['flags']:
        template['num_args'] = [0]
        template['flags'] = {"--abort": [0]}

    else:
        template['num_args'] = [1]
        template['flags'] = {"-m": [1], '-X': [1]}

    outs, errs = finish_command(command, template, log)
    if 'CONFLICT' in outs + errs:
        log['conflict'] = True

    return outs, errs


def git_rebase_handler(command, log, num_args=None):
    template = {
        'on_success': ['git_change', 'tree_change']
    }

    if '--continue' in command['flags']:
        template['num_args'] = [0]
        template['flags'] = {"--continue": [0]}

    elif '--abort' in command['flags']:
        template['num_args'] = [0]
        template['flags'] = {"--abort": [0]}

    else:
        template['num_args'] = [1] if num_args is None else '+'
        template['flags'] = {'-X': [1]}

    outs, errs = finish_command(command, template, log)
    if 'CONFLICT' in outs + errs:
        log['conflict'] = True

    return outs, errs


def git_cherry_pick_handler(command, log):  # Okazuje się, że z grubsza cherry_pick jest tym samym co rebase
    return git_rebase_handler(command, log, num_args='+')


def git_log_handler(command, log):
    template = {
        'num_args': [0],
        'flags': {'--graph': [0], "--all": [0], "--oneline": [0], "--decorate": [0], "--reflog": [0]},
    }
    return finish_command(command, template, log)


def git_branch_handler(command, log):
    template = {
        'num_args': [0, 1],
        'flags': {'-d': [1], '-D': [1]},
        'on_success': ['tree_change']
    }
    return finish_command(command, template, log)


def git_status_handler(command, log):
    template = {
        'num_args': [0]
    }
    return finish_command(command, template, log)


def git_diff_handler(command, log):
    template = {
        'num_args': [0, 1, 2],
        'flags': {'--cached': [0]}
    }
    return finish_command(command, template, log)


def git_checkout_handler(command, log):
    template = {
        'num_args': [1],
    }
    return finish_command(command, template, log)


def list_of_words(command):
    ret = []
    beg = 0
    nawiasek = ""

    for i in range(len(command)):
        letter = command[i]
        if letter in "\"'":
            if nawiasek:
                if letter == nawiasek:  # kończę wystąpienie
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
        'flags': {}
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
            ret['flags'][words[flag_poz]] = words[flag_poz + 1:i]
            flag_poz = i

    if flag_poz != len(words):
        ret['flags'][words[flag_poz]] = words[flag_poz + 1:]

    return ret


def handle_command(command, log, sudo=None):
    if 'sudo' in session:
        sudo = True

    # if command.startswith('sudo '):
    #     outs, errs = raw_run(command[5:])
    #     return "SUDO", outs, errs
    
    if command == 'give sudo':
        if 'sudo' not in session:
            session['sudo'] = True
            session.modified = True
            return "GIVE SUDO HANDLER", "DODAJE PRAWA SUDO", ""
        else:
            return "GIVE SUDO HANDLER", "", "SUDO JUŻ PRZYZNANE"

    if command == 'take sudo':
        if 'sudo' in session:
            session.pop('sudo')
            session.modified = True
            return "TAKE SUDO HANDLER", "ZABIERAM UPRAWNIENIA SUDO", ""
        else:
            return "TAKE SUDO HANDLER", "", "SUDO NIE BYŁO PRZYZNANE"

    permission = 1
    if sudo:
        permission = 3

    print("Command: " + red(command))
    prohibited = '`><&|\\'
    for char in prohibited:
        if char in command:
            return 'niedozwolony znak', '', f"Nie pozwalamy na użycie znaku {char}"

    parsed_command = parse_command(command)
    if parsed_command['command'] == 'show':
        return "SHOW", "W razie potrzeby użyj 'help'", ""

    name = parsed_command['command']

    if len(name) == 0:  # nawias jest niepoprawny
        return "Nawiasy", "", "Jakiś nawias " + parsed_command['args'][0] + " jest bez pary"

    if name not in commands_cost:
        return "LOV PROVILEGE", "", "Nieprawidłowa komenda. Wpisz 'help', by zobaczyć aktualnie dozwolone komendy"

    extra_allowed = []

    level, stage = session['level'], session['stage']

    add_extra_allowed(extra_allowed)

    all_allowed = []
    for command_name, cost in commands_cost.items():
        if cost <= permission or command_name in extra_allowed:
            all_allowed.append(command_name)

    if name not in all_allowed:
        return "", "", "Ta komenda jest wyłączona na tym etapie poziomu"

    # te zmienne są nam potrzebne tylko dla funkcji 'commands' (domyślnie to ma być help/show)
    log['allowed'] = all_allowed

    commits_before = len(git_tree())
    outs, errs = globals()[name.replace(' ', '_').replace('-', '_') + "_handler"](parsed_command, log)
    commits_after = len(git_tree())
    log['stdout'] = outs
    log['stderr'] = errs
    log.pop('allowed')

    if name == 'init_level':
        return name + " HANDLER", outs, errs

    # sprawdzanie, czy nie osiągnęliśmy kolejnego 'stage'
    check_stage(log)

    # sprawdzanie, czy nie powinniśmy przejść do kolejnego poziomu
    # warunkiem sukcesu (poza poziomem, gdzie mamy git merge --abort)
    # jest takie samo drzewo git (z dokładnością do topologi*)
    # dlatego właśnie zakładamy, że po rozpoczęciu poziomu, drzewo git
    # ma o jeden mniej commit niż ma mieć domyślnie, i w momencie, gdy
    # wykonamy kolejną zmianę (dodającą commit), albo zwrócimy
    # informację o sukcesie, albo o resecie

    print(red(f"{commits_before = }"))
    print(green(f"{commits_after = }"))

    if level == 5:
        if commits_before < commits_after:
            log['reset'] = 'na tym poziomie nie chcemy tworzyć nowych commitów'
        elif len(errs) == 0 and name == 'git merge' and '--abort' in parsed_command['flags']:
            log['success'] = True

    elif commits_before < commits_after and name != 'reset':
        list_of_imported_git_trees = import_expected_git_tree(level)
        print("LICZBA POPRAWNYCH ROZWIĄZAŃ", red(str(len(list_of_imported_git_trees))))
        actual_tree = git_tree()

        def process_git_tree(tree):
            counter = 1
            map_of_hashes = {}

            for commit in tree:
                for child_hash in commit['children']:
                    if child_hash not in map_of_hashes:
                        map_of_hashes[child_hash] = counter
                        counter += 1
                for parent_hash in commit['parents']:
                    if parent_hash not in map_of_hashes:
                        map_of_hashes[parent_hash] = counter
                        counter += 1
                commit['message'] = '-'  # we do not care about the messages

        # comparing two trees
        def compare(tree1, tree2):
            if len(tree1) != len(tree2):
                return False

            for i in range(len(tree1)):
                commit1, commit2 = tree1[i], tree2[i]
                if len(commit1['children']) != len(commit2['children']) or \
                        commit1['branch'] != commit2['branch'] or \
                        commit2['branch'] != commit2['branch']:
                    return False

                for j in range(len(commit1['children'])):
                    if commit1['children'][j] != commit1['children'][j]:
                        return False

                for j in range(len(commit1['parents'])):
                    if commit1['parents'][j] != commit1['parents'][j]:
                        return False

            return True

        process_git_tree(actual_tree)
        found = False

        for imp_git_tree in list_of_imported_git_trees:
            process_git_tree(imp_git_tree)
            if compare(imp_git_tree, actual_tree):
                check_success(log)  # it will either 'fill' reset of 'success' flag
                found = True
                break

        if not found:
            log['reset'] = "Drzewo git jest inne od oczekiwanego"

    return name + " HANDLER", outs, errs
