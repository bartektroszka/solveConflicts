from flask import session
from .utils import paths, run_command
import os


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
                   "Drugą opcją jest podanie flagi --continue bez żandych argumentów"

    if '--continue' in command['flagi']:
        if len(command['flagi']['--continue']) == 0 and len(command['args']) == 0:
            outs, errs = run_command(session['cd'], 'git -c core.editor=true merge --continue')
        else:
            return "", help_message
    else:
        if '-m' not in command['flagi'] or len(command['flagi']['-m']) != 1 or len(command['args']) != 1:
            return "", help_message

        outs, errs = run_command(session['cd'], 'git merge ' + command['args'][0] + ' -m ' + command['flagi']['-m'][0])

    log['git_change'] = log['tree_change'] = True
    if 'conflict' in (outs + errs).lower():
        log['conflict'] = True

    return outs, errs


def git_rebase_handler(command, log):
    help_message = "Dla 'git rebase' należy podać jeden argument (hash commita, albo nazwę brancha)" + \
                   "\nDrugim sposobem użycia jest podanie tylko flagi --continue"

    if '--continue' in command['flagi']:
        if len(command['flagi']['--continue']) == 0 and len(command['args']) == 0:
            outs, errs = run_command(session['cd'], 'git -c core.editor=true rebase --continue')
        else:
            return "", help_message
    else:
        if len(command['flagi']) != 0 or len(command['args']) != 1:
            return "", help_message

        outs, errs = run_command(session['cd'], 'git rebase ' + command['args'][0])

    log['git_change'] = log['tree_change'] = True
    if 'conflict' in (outs + errs).lower():
        log['conflict'] = True

    return outs, errs


def git_cherry_pick_handler(command, log):
    # TODO
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

    if len(command['args']) > 2:
        return "", "Za dużo argumentów (zero, jeden albo dwa)"

    return run_command(session['cd'], f"git diff {' '.join(command['args'])}")


def git_stash_handler(command, log):
    return "TODO", "TODO"


def git_checkout_handler(command, log):
    if len(command['flagi']) != 0:
        return "", "Nie pozwalamy na podawanie flag do komendy 'git diff'"

    if len(command['args']) != 1:
        return "", "Podaj dokładnie jedne argument (nazwę gałęzi)"

    log['git_change'] = True

    return run_command(session['cd'], f"git checkout {command['args'][0]}")
