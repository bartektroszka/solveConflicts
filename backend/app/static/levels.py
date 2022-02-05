import json
import os
from flask import session
from .utils import green, no_spaces, app_folder, user_folder_path


def hint_handler(command, log):
    level = session['level']
    stage = session['stage']

    if level == 1:
        if stage == 1:
            return "Użyj komendy 'git merge friend_branch -m <wiadomość>'", ""
        if stage == 2:
            return "Pozbądź się konflitku a potem wpisz 'git add przepis.txt' i " \
                   "'git merge --continue' lub 'git commit -m <wiadomość>'. Pamiętaj, że musisz zachować dokładnie " \
                   "jedną z wersji przepisu (twoją, albo przyjaciela)", ""

    elif level == 2:
        if stage == 1:
            return "Użyj komendy 'git merge friend_branch -m <wiadomość>'", ""
        if stage == 2:
            return "Pozbądź się konflitku a potem wpisz 'git add style.json' i " \
                   "'git merge --continue' lub 'git commit -m <wiadomość>'. W pliku json " \
                   "style.json masz zostawić swoją wersję części 'header' i cudzą wersję 'footer'.", ""

    elif level == 3:
        if stage == 1:
            return "Użyj komendy 'git rebase liczby_catalana'", ""
        if stage == 2:
            return "Pozbądź się konflitku, a potem wpisz 'git rebasee --continue'\n" + \
                   "Pamiętaj, że na tym poziomie masz zostawić jedną z wersji funckji 'silnia' oraz " \
                   "dokończone implementacje funkcji 'taylor_e' oraz 'catalan'", ""

    elif level == 4:
        if stage == 1:
            return "Użyj komendy 'git cherry-pick <COMMIT>' gdzie commit to ciąg przynajmniej 4 znaków " \
                   "z hasza commita z komentarzem 'helpful defines'", ""

        if stage == 2:
            return "Pozbądź się konflitku, a potem wpisz 'git cherry-pick --continue'\n" + \
                   "Zaaplikuj wszystkie zmiany z drugiej gałęzi.", ""

    elif level == 5:
        if stage == 1:
            return "Użyj komendy 'git merge friend_branch -m <wiadomość>", ""
        if stage == 2:
            return "Użyj komendy 'git merge --abort", ""

    elif level == 6:
        if stage == 1:
            return "Użyj komendy 'git merge mat -m <wiadomość>", ""
        if stage == 2:
            return "Pozbądź się niepotrzebnych zmian z pliku wyjazd.txt, a następnie powtórz merge", ""

    elif level == 7:
        if stage == 1:
            return "Użyj komendy 'git merge rodzice -m <wiadomość>", ""
        if stage == 2:
            return "Konflikt jest dośc spory. I tak wiesz, że musisz się zgodzić na wszystkie zmiany rodziców "\
                   "więc najlepiej przerwać aktualnego merge za pomocą --abort i zrobić merge z flagą '-X theirs'", ""

    elif level == 8:
        if stage == 1:
            return "Możesz spróbować zrobić ten poziom na dwa sposoby. Albo po prostu używając od razu"\
                   "'git commit', albo najpierw wykonać checkout na gałąź dfsFix i tam 'git rebase master'", ""
        if stage == 2:
            return "Konflikt polega na tym, że na gałęzi master zamieniono nazwy zmiennych 'w' oraz 'x' na"\
                   "odpowiednio 'startowy' i 'aktualny'. Zaaplikuj zmianę z dfsFix z nowymi zmiennymi!", ""

    return "", "ERROR"


def check_stage(log):
    level = session['level']
    stage = session['stage']

    if 1 <= level <= 5 or level == 7 or level == 8:
        if stage == 1 and 'conflict' in log:
            session['stage'] = 2
            session.modified = True

    elif level == 6:
        if log['stderr'].startswith('error: Your local changes to the'):
            session['stage'] = 2
            session.modified = True

    else:
        pass


def add_extra_allowed(extra_allowed):
    # Do ustalenia jest jeszcze to na jakie komendy pozwalamy na danych levelach

    level = session['level']
    stage = session['stage']

    if level == 1 or level == 2:
        extra_allowed.append('git add')
        extra_allowed.append('git merge')
        if stage == 2:
            extra_allowed.append('git commit')

    elif level == 3:
        extra_allowed.append('git rebase')
        extra_allowed.append('git add')

    elif level == 4:
        extra_allowed.append('git cherry-pick')
        extra_allowed.append('git add')

    elif level == 5:
        extra_allowed.append('git merge')

    elif level == 6:
        extra_allowed.append('git merge')
        extra_allowed.append('git add')

    elif level == 7:
        extra_allowed.append('git merge')
        extra_allowed.append('git add')

    elif level == 8:
        extra_allowed.append('git merge')
        extra_allowed.append('git rebase')
        extra_allowed.append('git add')
        extra_allowed.append('git branch')
        extra_allowed.append('git checkout')

    else:
        pass  # TODO level 6, 7 i 8.


def check_success(log):
    # W tym momencie zakładamy, że dokonał się merge i drzewa są takie same
    # czasami chcemy jednak sprawdzić, czy wartość niektórych plików jest
    # taka, jak tego oczekujemy od użytkowników

    level = session['level']
    level_directory = os.path.join(app_folder(), 'levels', f'level{level}')
    if level == 1:
        with open(os.path.join(level_directory, 'friend_file'), 'r') as f:
            expected1 = no_spaces(f.read())
        with open(os.path.join(level_directory, 'your_file'), 'r') as f:
            expected2 = no_spaces(f.read())

        try:
            with open(os.path.join(user_folder_path(), 'przepis.txt'), 'r') as f:
                user_output = no_spaces(f.read())
        except FileNotFoundError:
            log['reset'] = 'Nie ma pliku przepis.txt'
            return

        print(f"{expected1 = }")
        print(f"{expected2 = }")
        print(f"{user_output =}")

        if expected1 == user_output or expected2 == user_output:
            log['success'] = True
        else:
            log['reset'] = "Zawartość pliku 'przepis.txt' niezgodna z poleceniem"

    elif level == 2:
        with open(os.path.join(level_directory, 'expected_answer.json')) as f:
            expected_output = json.load(f)

        try:
            with open(os.path.join(user_folder_path(), 'style.json')) as f:
                try:
                    user_output = json.load(f)
                except json.JSONDecodeError:
                    log['reset'] = "Zawartość pliku 'style.json' nie jest w poprawnym formacie JSON!"
                    return

        except FileExistsError:
            log['reset'] = "Nie ma pliku 'style.json'"
            return False

        if expected_output != user_output:
            log['reset'] = "Oczekiwano innej zawartości pliku 'style.json'"
            return

        log['success'] = True

    elif level == 3:
        ok = False
        try:
            with open(os.path.join(user_folder_path(), 'kod.py'), 'r') as f:
                user_output = no_spaces(f.read())
        except FileNotFoundError:
            log['reset'] = 'Nie ma pliku kod.py'
            return

        for i in range(4):
            with open(os.path.join(level_directory, f'expected_output{i}.py'), 'r') as f:
                expected_output = no_spaces(f.read())
                if expected_output == user_output:
                    ok = True
        if ok:
            log['success'] = True
        else:
            log['reset'] = "Niepoprawna zawartośc pliku kod.py"

    elif level == 4:
        try:
            with open(os.path.join(user_folder_path(), 'kod.cpp'), 'r') as f:
                user_output = no_spaces(f.read())
        except FileNotFoundError:
            log['reset'] = 'Nie ma pliku kod.cpp'
            return

        with open(os.path.join(level_directory, f'friend_kod2.cpp'), 'r') as f:
            expected_output = no_spaces(f.read())

        if user_output == expected_output:
            log['success'] = True
        else:
            log['reset'] = "Niepoprawna zawartośc pliku kod.cpp"

    elif level == 5:
        pass  # sprawdzenia dokonujemy wcześniej w module commands.py

    elif level == 6:
        out_file = 'wyjazd.txt'
        try:
            with open(os.path.join(user_folder_path(), out_file), 'r') as f:
                user_output = no_spaces(f.read())
        except FileNotFoundError:
            log['reset'] = f'Nie ma pliku {out_file}'
            return

        with open(os.path.join(level_directory, f'comb.txt'), 'r') as f:
            expected_output = no_spaces(f.read())

        if user_output == expected_output:
            log['success'] = True
        else:
            log['reset'] = f"Niepoprawna zawartośc pliku {out_file}"

    elif level == 7:
        out_files = ['ogrod.txt',
                     os.path.join('parter', 'kuchnia.txt'),
                     os.path.join('parter', 'salon.txt'),
                     os.path.join('pietro', 'lazienka.txt'),
                     os.path.join('pietro', 'garderoba.txt'),
                     os.path.join('pietro', 'sypialnia.txt'),
                     ]

        for file in out_files:
            try:
                with open(os.path.join(user_folder_path(), file), 'r') as f:
                    user_output = no_spaces(f.read())
            except FileNotFoundError:
                log['reset'] = f'Nie ma pliku {file}'
                return

            with open(os.path.join(level_directory, 'ogrod', file), 'r') as f:
                expected_output = no_spaces(f.read())

            if user_output != expected_output:
                log['reset'] = f"Niepoprawna zawartośc pliku {file}"
                return

            log['success'] = True

    elif level == 8:
        try:
            with open(os.path.join(user_folder_path(), 'kod.py'), 'r') as f:
                user_output = no_spaces(f.read())
        except FileNotFoundError:
            log['reset'] = f'Nie ma pliku kod.py'
            return

        with open(os.path.join(level_directory, 'expected_output.py'), 'r') as f:
            expected_output = no_spaces(f.read())

        if user_output != expected_output:
            print(f"{user_output}")
            print(f"{expected_output}")
            log['reset'] = f"Niepoprawna zawartośc pliku 'kod.py'"
            return

        log['success'] = True

    else:
        log['reset'] = "Przeszedłeś wszystkie poziomy!"
        return
