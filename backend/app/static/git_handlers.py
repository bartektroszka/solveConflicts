from flask import session
from .utils import paths, run_command
import os


def git_restore_handler(command, log):
    help_message = "Git restore, przyjmuje przynajmniej jeden argument. Nie pozwalamy na żadne flagi dla tej komendy."

    args = command['args']
    if len(args) == 0:
        return "", help_message

    if len(command['flagi']) != 0:
        return "", "Nie pozwalamy na podawanie żadnych flag do komendy git restore!"

    log['tree_change'] = log['git_change'] = True
    shell_command = f"git restore {' '.join(args)}"
    return run_command(session['cd'], shell_command)


def git_stash_handler(command, log):
    help_message = "Git stash, przyjmuje jeden lub dwa argumenty. Pierwszy argument może być jednym z pięciu poleceń " \
                   "[save, pop, drop, clear, apply]. Jeżeli jest to save, drop, lub apply, to należy podać drugi." \
                   "argument."

    args = command['args']
    if len(args) == 0 or len(args) > 2:
        return "", help_message

    if len(command['flagi']) != 0:
        return "", "Nie pozwalamy na podawanie żadnych flag do komendy git stash!"

    jeden = ['pop', 'clear']
    dwa = ['save', 'drop', 'apply']

    if (len(args) == 1 and args[0] not in jeden) or (len(args) == 2 and args[0] not in dwa):
        return "", help_message

    log['tree_change'] = log['git_change'] = True
    shell_command = f"git stash {args[0]} {args[1] if len(args) == 2 else ''}"
    return run_command(session['cd'], shell_command)


def git_add_handler(command, log):
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
        return "", "Po komendzie git commit należy dodać flagę -m, a później wiadomość komita"

    for flaga, lista in command['flagi'].items():
        if flaga != '-m':
            return "", "Dla komendy 'git commit' pozwalamy jedynie na podanie flagi '-m' z jednym argumentem"
        if len(lista) != 1:
            return "", "Flaga -m musi przyjąć dokładnie jeden argument"

    log['git_change'] = True
    return run_command(session['cd'], f"git commit -m {command['flagi']['-m'][0]}")


def git_merge_handler(command, log):
    help_message = "Dla 'git merge' należy podać jeden argument (nazwę gałęzi), a potem dać flagę -m z wiadomością. " \
                   "Działa też flaga -X (z jednym argumentem 'theirs' albo 'ours'\n" \
                   "Drugą opcją jest podanie tylko flagi --continue bez żadnych argumentów\n" + \
                   "Trzecią opcją jest podanie tylko flagi --abort bez żadnych argumentów"

    if '--continue' in command['flagi']:
        if len(command['flagi']['--continue']) == 0 and len(command['args']) == 0:
            outs, errs = run_command(session['cd'], 'git -c core.editor=true merge --continue')
        else:
            return "", help_message

    elif '--abort' in command['flagi']:
        if len(command['flagi']['--abort']) == 0 and len(command['args']) == 0 and len(command['flagi']) == 1:
            outs, errs = run_command(session['cd'], 'git merge --abort')
        else:
            return "", help_message

    else:
        if '-m' not in command['flagi'] or len(command['args']) != 1:
            return "", help_message

        dozwolone_flagi = ['-m', '-X']
        for flaga in command['flagi'].keys():
            if flaga not in dozwolone_flagi:
                return "", f"Flaga {flaga} nie jest dozwolona dla tej komendy"

        if '-X' in command['flagi'] and len(command['flagi']['-X']) != 1:
            return "", "Zła liczba argumentów dla flagi -X (ma być dokładnie jeden)"

        if len(command['flagi']['-m']) != 1:
            return "", "Trzeba podać dokładnie jedną wiadomość dla flagi '-m'"

        flagi = " "
        for flaga, flag_args in command['flagi'].items():
            flagi += flaga + ' ' + ' '.join(flag_args) + ' '
        args = ' ' + ' '.join(command['args'])
        outs, errs = run_command(session['cd'], command['command'] + args + flagi)

    log['git_change'] = log['tree_change'] = True
    if 'conflict' in (outs + errs).lower():
        log['conflict'] = True

    return outs, errs


def git_rebase_handler(command, log):
    help_message = "Dla 'git rebase' należy podać jeden argument (hasz komita, albo nazwę brancha). Obsługujemy " \
                   "flagę -X z jednym argumentem (np 'theirs' albo 'ours')\n" + \
                   "Drugim sposobem użycia jest podanie tylko flagi --continue\n" + \
                   "Trzeci sposobem użycia jest podanie tylko flagi --abort"

    if '--continue' in command['flagi']:
        if len(command['flagi']['--continue']) == 0 and len(command['args']) == 0 and len(command['flagi']) == 1:
            outs, errs = run_command(session['cd'], 'git rebase --continue')
        else:
            return "", help_message

    elif '--abort' in command['flagi']:
        if len(command['flagi']['--abort']) == 0 and len(command['args']) == 0 and len(command['flagi']) == 1:
            outs, errs = run_command(session['cd'], 'git rebase --abort')
        else:
            return "", help_message

    else:
        if len(command['args']) != 1:
            return "", help_message

        dozwolone_flagi = ['-X']
        for flaga in command['flagi'].keys():
            if flaga not in dozwolone_flagi:
                return "", f"Flaga {flaga} nie jest dozwolona dla tej komendy"

        if '-X' in command['flagi'] and len(command['flagi']['-X']) != 1:
            return "", "Zła liczba argumentów dla flagi -X (ma być dokładnie jeden)"

        flagi = " "
        for flaga, flag_args in command['flagi'].items():
            flagi += flaga + ' ' + ' '.join(flag_args) + ' '
        args = ' ' + ' '.join(command['args'])
        outs, errs = run_command(session['cd'], command['command'] + args + flagi)

    log['git_change'] = log['tree_change'] = True
    if 'conflict' in (outs + errs).lower():
        log['conflict'] = True

    return outs, errs


def git_cherry_pick_handler(command, log):
    help_message = "git cherry-pick -- należy podać listę komitów (można też podać '-X theirs' / '-X ours')\n" \
                   "Drugim sposobem użycia jest podanie tylko flagi --continue\n" \
                   "Trzeci sposobem użycia jest podanie tylko flagi --abort"

    if '--continue' in command['flagi']:
        if len(command['flagi']['--continue']) == 0 and len(command['args']) == 0 and len(command['flagi']) == 1:
            outs, errs = run_command(session['cd'], 'git -c core.editor=true cherry-pick --continue')
        else:
            return "", help_message

    elif '--abort' in command['flagi']:
        if len(command['flagi']['--abort']) == 0 and len(command['args']) == 0 and len(command['flagi']) == 1:
            outs, errs = run_command(session['cd'], 'git -c core.editor=true cherry-pick --abort')
        else:
            return "", help_message

    else:
        dozwolone_flagi = ['-X']
        for flaga in command['flagi'].keys():
            if flaga not in dozwolone_flagi:
                return "", f"Flaga {flaga} nie jest dozwolona dla tej komendy"

        if '-X' in command['flagi'] and len(command['flagi']['-X']) != 1:
            return "", "Zła liczba argumentów dla flagi -X (ma być dokładnie jeden)"

        flagi = " "
        for flaga, flag_args in command['flagi'].items():
            flagi += flaga + ' ' + ' '.join(flag_args) + ' '
        args = ' ' + ' '.join(command['args'])
        outs, errs = run_command(session['cd'], command['command'] + args + flagi)

    log['git_change'] = log['tree_change'] = True
    if 'conflict' in (outs + errs).lower():
        log['conflict'] = True

    return outs, errs


def git_log_handler(command, log):
    dozwolone_flagi = ['--graph', '--all', '--oneline', '--decorate', '--reflog']

    for flaga, lista in command['flagi'].items():
        if flaga not in dozwolone_flagi:
            return "", f"Niedozwolona flaga {flaga} (można używać {dozwolone_flagi})"
        if len(lista):
            return "", f"Flaga {flaga} nie może posiadać żadnego argumentu"

    if len(command['args']):
        return "", "Nie pozwalamy na podawanie argumentów do 'git log'"

    return run_command(session['cd'], f"git log {' '.join(command['flagi'].keys())}")


def git_branch_handler(command, log):
    if len(command['args']) > 1:
        return "", "Za dużo argumentów (0 - wypisanie listy gałęzi, 1 - stworzenie nowej gałęzi)"

    dozwolone_flagi = ['-d', '-D']
    for flaga in command['flagi'].keys():
        if flaga not in dozwolone_flagi:
            return "", f"Flaga {flaga} nie jest dozwolona dla tej komendy"

    flagi = " "
    for flaga, flag_args in command['flagi'].items():
        flagi += flaga + ' ' + ' '.join(flag_args) + ' '
    args = ' ' + ' '.join(command['args'])

    log['git_change'] = True

    return run_command(session['cd'], command['command'] + args + flagi)


def git_status_handler(command, log):
    if len(command['args']) or len(command['flagi']):
        return "", "Nie pozwalamy na podawanie argumentów i flag do komendy 'git status'"

    if len(command['flagi']) != 0:
        return "", "Nie pozwalamy na podawanie flag do komendy 'ls'!"

    return run_command(session['cd'], "git status")


def git_diff_handler(command, log):
    if len(command['flagi']) != 0:
        return "", "Nie pozwalamy na podawanie flag do komendy 'git diff'"

    if len(command['args']) > 2:
        return "", "Za dużo argumentów (zero, jeden albo dwa)"

    return run_command(session['cd'], f"git diff {' '.join(command['args'])}")


def git_checkout_handler(command, log):
    if len(command['flagi']) != 0:
        return "", "Nie pozwalamy na podawanie flag do komendy 'git diff'"

    if len(command['args']) != 1:
        return "", "Podaj dokładnie jedne argument (nazwę gałęzi)"

    log['git_change'] = True

    return run_command(session['cd'], f"git checkout {command['args'][0]}")
