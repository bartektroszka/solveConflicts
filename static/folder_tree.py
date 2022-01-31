import io
import os
import re
from flask import session

from .utils import red, run_command
from itertools import count

my_counter = count()


def recurse_over_tree(current_path, tree):
    if not isinstance(tree, dict) or 'items' not in tree.keys():
        return "[ERROR] incorrect tree specification"

    list_of_dirs, list_of_files = [], []

    for subdir, dirs, files in os.walk(current_path):
        list_of_dirs = [os.path.join(current_path, directory) for directory in dirs]
        list_of_files = [os.path.join(current_path, file) for file in files]
        break

    my_list_of_dirs, my_list_of_files = [], []

    for element in tree['items']:
        new_path = os.path.join(current_path, element['label'])
        if 'items' in element.keys():
            my_list_of_dirs.append(new_path)
        else:
            my_list_of_files.append(new_path)

    # TODO
    for directory in list_of_dirs:
        if directory not in my_list_of_dirs:
            print(f"rm -r {directory} [command not run for safety reasons]")
    for file in list_of_files:
        if file not in my_list_of_files:
            print(f"rm {file}, [command not run for safety reasons]")

    for element in tree['items']:
        if not isinstance(element, dict):
            return "[ERROR] incorrect tree specification"

        new_path = os.path.join(current_path, element['label'])
        if 'data' in element.keys():
            # this is a file
            if not isinstance(element['data'], str):
                return "[ERROR] File data has to be a string"
            os.popen(f"echo '{element['data']}' > {new_path}")
        else:
            if not 'items' in element.keys():
                return "[ERROR] Tree object has to have either items on data field!"

            if not os.path.isdir(new_path):
                try:
                    os.mkdir(new_path)
                except:
                    return "[ERROR] Problem with creating file"

            error_message = recurse_over_tree(new_path, element)
            if error_message != "no error":
                return error_message

    return "no error"


def get_directory_tree(path, ret, parent_id=None):
    if path not in session['folder_ids']:
        session['folder_ids'][path] = next(my_counter)
        session.modified = True
    if os.path.isdir(path):

        ret.append({
            'label': os.path.basename(path),
            'parentId': parent_id,
            'id': session['folder_ids'][path]
        })

        if parent_id is None:
            ret[-1]['label'] = 'Home'

        my_id = ret[-1]['id']
        ret[-1]['items'] = []

        phases = [os.path.isfile, os.path.isdir]  # na początku pliki, potem foldery

        for phase_function in phases:
            for filename in os.listdir(path):
                if filename[0] == '.':  # TODO omijanie ukrytych plików
                    continue
                full_filename = os.path.join(path, filename)

                if phase_function(full_filename):
                    get_directory_tree(full_filename, ret, my_id)

    else:  # Managing file
        if not os.path.isfile(path):
            return f"[ERROR] Path '{path}' leads neither to a file nor to a directory!"

        temp = {
            'label': os.path.basename(path),
            'parentId': parent_id,
            'id': session['folder_ids'][path]
        }

        try:
            with open(path, 'r') as f:
                temp['data'] = f.read()
        except:
            try:
                with io.open(path, "r", encoding="utf-8") as f:
                    temp['data'] = f.read()
            except:
                temp['data'] = "[ERROR] ------ problem with reading file data ------"

        ret[-1]['items'].append(temp)


def from_first_character(napis):
    for i in range(len(napis)):
        if napis[i].isalpha() or napis[i].isdigit():
            return napis[i:]
    return ""


def pozbac_sie_graph(info):
    return [from_first_character(line) for line in info]


def git_tree(user=None):
    if user is None:
        user = session['id']

    user_directory = os.path.join(os.getcwd(), 'users_data', user)

    if not os.path.isdir(os.path.join(user_directory, '.git')):
        return []

    try:  #
        info_raw, errs = run_command(user_directory, "git log --pretty=raw --graph --all --reflog")
        info_oneline, errs = run_command(user_directory, "git log --oneline --graph --all --decorate --reflog")
        info_raw = info_raw.split('\n')
        info_oneline = info_oneline.split('\n')

    except BaseException as exception_message:
        print(red("[ERROR]" + str(exception_message)))
        raise

    # tworzenie commitów
    list_of_commits = []
    dict_of_commits = {}
    len_of_hashes = -1

    # potrzebujemy kolejności z --graph, ale nie chcemy tych znaków, które są tam na początku
    info_oneline = pozbac_sie_graph(info_oneline)
    info_raw = pozbac_sie_graph(info_raw)

    for line in reversed(info_oneline):
        pom = line.split()
        if len(pom) <= 1:
            continue

        commit = {}
        commit['hash'] = pom[0]
        len_of_hashes = len(commit['hash'])
        commit['parents'] = []
        commit['children'] = []

        mam_branche = pom[1][0] == '('
        if mam_branche:
            nawiaski = re.split('\(|\)', line)
            branches = nawiaski[1].split(',')
            commit['message'] = nawiaski[2].strip()

            commit['branch'] = branches[0]  # bierzemy tylko jednego brancha nawet jak jest ich kilka w jednym commicie
        else:
            if 'branch' not in commit:
                commit['branch'] = 'DETACHED'
            commit['message'] = line[len(pom[0]):].strip()

        list_of_commits.append(commit)
        dict_of_commits[commit['hash']] = commit

    # updatowanie polaczen w grafie
    current_commit = 'nic_tu_niema'

    for line in info_raw:
        temp = line.split()
        if line.startswith('commit'):
            current_commit = temp[1][:len_of_hashes]
        if line.startswith('parent'):
            parent_hash = temp[1][:len_of_hashes]

            # wszystkim ojcom propaguje info o swoim branchu (jeżeli już nie mają brancha)
            if 'branch' not in dict_of_commits[parent_hash] or dict_of_commits[parent_hash]['branch'] == 'DETACHED':
                dict_of_commits[parent_hash]['branch'] = dict_of_commits[current_commit]['branch']

            dict_of_commits[current_commit]['parents'].append(parent_hash)
            dict_of_commits[parent_hash]['children'].append(current_commit)

    # return info_oneline, info_raw, list_of_commits
    return list_of_commits


def merge_commit_count(user):
    return len([commit for commit in git_tree(user) if len(commit['parents']) >= 2])
