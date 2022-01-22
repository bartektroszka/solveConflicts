import json
import os
from flask import session


def check_success(ret):
    command = ret['command']
    level = ret['level']
    merged = ret['merged']

    split = command.split()
    if len(split) and split[0] == 'init_level':
        ret['success'] = False
        return

    if level == 1:
        ret['success'] = merged
        return

    if level == 2:
        if not merged:
            ret['success'] = False
            return

        with open(os.path.join('levels', 'level2', 'expected_answer.json')) as f:
            expected_output = json.load(f)

        try:
            with open(os.path.join('users_data', session['id'], 'style.json')) as f:
                try:
                    user_output = json.load(f)
                except json.JSONDecodeError:
                    ret['success'] = False
                    ret['reset'] = "Zawartość pliku 'style.json' nie jest w poprawnym formacie JSON!"
                    return

        except FileExistsError:
            ret['success'] = False
            ret['reset'] = "Nie ma pliku 'style.json'"
            return False

        if expected_output != user_output:
            ret['success'] = False
            ret['reset'] = "Oczekiwano innej zawartości pliku 'style.json'"
            return

        ret['success'] = True
        return

    if level == 3:
        ret['success'] = merged
        return

    if level == 4:
        ret['success'] = merged
        return

    if level == 4:
        ret['success'] = merged
        return

    if level == 5:
        ret['success'] = merged
        return

    assert False
