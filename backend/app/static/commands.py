from .utils import import_expected_git_tree
from .folder_tree import git_tree
from .levels import check_success, check_stage, add_extra_allowed
from .handlers import *
from .git_handlers import *

commands_cost = {
    'ls': 1,
    'touch': 1,
    'mkdir': 1,
    'pwd': 1,
    'hint': 1,
    'git log': 1,
    'git status': 1,
    'git diff': 1,
    'list': 1,

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

    'init_level': 3,
    'show_level': 3
}

short_help_messages = {
    'ls': "ls [DIR]",
    'touch': "touch +<FILE>",
    'mkdir': "mkdir +<DIR>",
    'pwd': "pwd",
    'hint': "hint",
    'git log': "git log [--graph] [--all] [--oneline] [--decorate]",
    'git status': "git status",
    'git diff': "git diff [COMMIT]",
    'list': "list +[COMMAND]",

    'cd': "cd <DIR>",
    'rm': "rm +<DIR/FILE>",
    'rmdir': "rmdir +<DIR/FILE>",
    'git add': "git add +<DIR/FILE>",
    'git commit': "git commit -m <MESSAGE>",
    'git rebase': "git rebase <BRANCH/COMMIT> -m <MESSAGE>\n git rebase --continue\n git rebase --abort",
    'git cherry-pick': "git cherry-pick +<COMMIT> -m <MESSAGE>\n git cherry-pick --continue\n git cherry-pick --abort",
    'git branch': "git branch\n git branch [-d] <BRANCH>",
    'git checkout': "git checkout [-b] <BRANCH>",  # TODO
    'git merge': "git merge <BRANCH> -m <MESSAGE>\n git merge --continue\n git merge --abort",

    'init_level': "init_level <LEVEL NUMBER> // ADMIN COMMAND",
    'show_level': "show_level // ADMIN COMMAND"
}

long_help_messages = {
    'ls': "ls -- komenda do wypisywania zawartości katalogu",
    'touch': "touch -- komenda do tworzenia nowych plików",
    'mkdir': "mkdir -- komenda do tworzenia nowych katalogów",
    'pwd': "pwd -- komenda do wypisywania ścieżki aktualnego katalogu",
    'hint': "hint -- komenda, której celem jest nakierowanie na rozwiązanie poziomu",
    'git log': "git log -- komenda do wypisywania aktualnego stanu grafu repozytorium",
    'git status': "git status -- komenda do sprawdzenia statusu repozytorium",
    'git diff': "git diff -- komenda pokazująca różnice między z aktualnym commitem. Podając argument w formie hasha " +
                "podajemy z jakim commitem chcemy się porównać. Można nie podawać arguemntów i wtedy dostaniemy " +
                "po prostu informację o aktualnych konfliktach (np. w trwającym merge).",
    'list': "list -- Pokaż aktualnie dostępne komendy. Zbiór komend może się zmieniać pomiędzy " +
            "poziomami, a nawet pomiędzy poszczególnymi etapami poziomów. Jako argument można podać " +
            "komendę, by uzyskać o niej bardziej szczegółowe informacje.",

    'cd': "cd -- zmień aktualny katalog",
    'rm': "rm -- usuń plik",
    'rmdir': "rmdir -- usuń katalog",
    'git add': "git add -- dodaj pliki do 'staging area' w celu późniejszego ich skomitowania",
    'git commit': "git commit -- zapisz zmiany w drzewie repozytorium (tworzy nowy wierzchołek w grafie)",
    'git merge': "git merge -- połącz dwie gałęzie. Wymuszamy podanie flagi -m. Można również użyć opcji --continue" +
                 "--continue by kontynuować merge po naprawieniu zmian, albo --abort do odrzucenia zmian ",
    'git rebase': "git rebase -- spróbuj podpiąć gałąź do innego miejsca w drzewie. Celowo wymuszamy, żeby zawsze " +
                  "przy tej operacji podawać wiadomość o zmianie. Można użyć też wersji git rebase --continue, albo " +
                  "git rebase --abort do odpowiednio kontuacji rebase po rozwiązaniu konfliktu, albo porzucenia zmian.",
    'git cherry-pick': "git cherry-pick -- wyłuskaj odpowiednie commity do swojej gałęzi. Wymuszamy podanie flagi -m." +
                       "Podobnie jak przy merge i rebase mamy flagi --continue i --abort",
    'git branch': "git branch -- stwórz albo usuń (flaga -d) gałąź",
    'git checkout': "git checkout -- przejdź na inną gałąź (flaga -b tworzy nową gałąź)",

    'init_level': "init_level -- wymuś zainicjalizowanie jakiegoś poziomu",
    'show_level': "show_level -- pokaż aktualny poziom i stage"
}


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


def list_handler(command, log):  # ten jeden handler zostanie tutaj, bo ma dostęp do zmiennych globalnych
    allowed = log['allowed']

    outs = '<> - obowiązkowe pole\n[] - opcjonalne pole\n+ oznacza jedno lub więccej pól\n'
    if len(command['args']) == 0:
        # wypisujemy wszystkie dostępne na tym poziomie komendy (w skrócie)
        for command_name in allowed:
            outs += short_help_messages[command_name] + '\n'

        outs += "\nWięcej informacji po wpisaniu konkretnej komendy np:\n'list \"git diff\" rmdir'"

    else:
        for flag, flag_args in command['flagi'].items():
            return "", f"Komenda 'list' nie oczekuje flagi {flag}"

        def no_parentheses(string):
            if string[0] == string[-1] and string[0] in "'\"":
                string = string[1:-1]
            return string

        command['args'] = [no_parentheses(com) for com in command['args']]

        for command_name in command['args']:
            if command_name not in commands_cost:
                return "", f"Niepoprawna komenda {command_name}"

        for command_name in command['args']:
            if command_name not in allowed:
                return "", f"Komenda {command_name} nie jest dostępna na tym etapie poziomu"

        for command_name in command['args']:
            outs += short_help_messages[command_name] + '\n' + long_help_messages[command_name] + '\n\n'

    return outs, ""


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

    if len(name) == 0:  # nawias jest niepoprawny
        return "Nawiasy", "", "Jakiś nawias " + parsed_command['args'][0] + " jest bez pary"

    if name not in commands_cost:
        return "LOV PROVILEGE", "", "Nieprawidłowa komenda. Wpisz 'list', by zobaczyć dozwolone komendy"

    extra_allowed = []

    level, stage = session['level'], session['stage']

    add_extra_allowed(extra_allowed)

    all_allowed = []
    for command_name, cost in commands_cost.items():
        if cost <= permission or command_name in extra_allowed:
            all_allowed.append(command_name)

    if name not in all_allowed:
        return "", "", "Ta komenda jest wyłączona na tym etapie poziomu"

    # te zmienne są nam potrzebne tylko dla funckcji 'commands' (domyślnie to ma być help/show)
    log['allowed'] = all_allowed

    commits_before = len(git_tree())
    outs, errs = globals()[name.replace(' ', '_').replace('-', '_') + "_handler"](parsed_command, log)
    commits_after = len(git_tree())

    log.pop('allowed')

    if name == 'init_level':
        return name + " HANDLER", outs, errs

    # sprawdzanie, czy nie osiągnęliśmy kolejnego 'stage'
    check_stage(log)

    # sprawdzanie, czy nie powinniśmy przejść do kolejnego poziomu
    # warunkiem sukcesu (poza poziomem, gdzie mamy git merge --abort)
    # jest takie samo drzewo git (z dokładnością do topologi*)
    # dlatego właśnie zakładamy, że po zainicjalizowaniu, drzewo git
    # ma o jeden mniej komit niż ma mieć domyślnie, i w momencie, gdy
    # wykonamy kolejną zmianę (dodającą commit), albo zwrócimy
    # informację o sukcesie, albo o resecie

    if level == 5:
        if commits_before < commits_after:
            log['reset'] = 'na tym poziomie nie chcemy tworzyć nowych commitów'
        elif len(errs) == 0 and name == 'git merge' and '--abort' in parsed_command['flagi']:
            log['success'] = True

    # sprawdzamy czy mamy takie same drzewo git porównujemy topologie oraz nazwy branchy
    # TODO może będą level gdzie dodajemy więcej niż jeden node???
    elif commits_before < commits_after:
        imported_git_tree = import_expected_git_tree(level)
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

        process_git_tree(imported_git_tree)
        process_git_tree(actual_tree)

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

        if compare(imported_git_tree, actual_tree):
            check_success(log)  # it will either 'fill' reset of 'success' flag
        else:
            log['reset'] = "Drzewo git jest inne od oczekiwanego"

    return name + " HANDLER", outs, errs
