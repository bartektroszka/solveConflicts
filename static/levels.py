import json
import os
from flask import session
from .utils import green


def no_spaces(string):
    return string.replace(" ", "").replace("\t", "").replace("\n", "")


def check_stage(log):
    level = session['level']
    stage = session['stage']

    if level == 1 or level == 2:
        if stage == 1 and 'conflict' in log:
            session['stage'] = 2
            session.modified = True
    else:
        pass


def add_extra_allowed(extra_allowed):
    level = session['level']
    stage = session['stage']

    if level == 1 or level == 2:
        extra_allowed.append('git add')
        extra_allowed.append('git merge')
        if stage == 2:
            extra_allowed.append('git commit')
    else:
        pass  # TODO


def check_success(log):
    # W tym momencie zakładamy, że dokonał się merge i drzewa są takie same
    # czasami chcemy jednak sprawdzić, czy wartość niektórych plików jest
    # taka, jak tego oczekujemy od użytkowników

    level = session['level']
    if level == 1:
        with open(os.path.join('levels', 'level1', 'friend_file'), 'r') as f:
            expected1 = no_spaces(f.read())
        with open(os.path.join('levels', 'level1', 'your_file'), 'r') as f:
            expected2 = no_spaces(f.read())

        try:
            with open(os.path.join('users_data', session['id'], 'przepis.txt'), 'r') as f:
                user_output = no_spaces(f.read())
        except FileNotFoundError:
            log['reset'] = 'Nie ma pliku przepis.txt'
            return

        if expected1 == user_output or expected2 == user_output:
            log['success'] = True
        else:
            log['reset'] = "Zawartość pliku 'przepis.txt' niezgodna z poleceniem"

    elif level == 2:
        with open(os.path.join('levels', 'level2', 'expected_answer.json')) as f:
            expected_output = json.load(f)

        try:
            with open(os.path.join('users_data', session['id'], 'style.json')) as f:
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
        return

    elif level == 4:
        return

    elif level == 4:
        return

    elif level == 5:
        return

    else:
        return
