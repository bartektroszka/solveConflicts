import os

from .utils import is_nick

from itertools import count

my_counter = count()

def recurse_over_tree(current_path, tree):  # TODO UKRYTE PLIKI
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


def get_directory_tree(path, len_of_prefix, parent_id=None):
    ret = {
        'label': path[len_of_prefix:],
        'parentId': parent_id,
        'id': next(my_counter)
    }

    if os.path.isdir(path):
        ret['items'] = []
        for filename in os.listdir(path):
            if filename[0] == '.':
                continue
            full_filename = os.path.join(path, filename)

            if os.path.isdir(full_filename) or os.path.isfile(full_filename):
                ret['items'].append(get_directory_tree(full_filename, len(path) + 1, ret['id']))

    else:
        if not os.path.isfile(path):
            return f"[ERROR] Path '{path}' leads neither to a file nor to a directory!"

        with open(path, 'r') as f:
            try:
                data = f.read()
            except:
                data = "[ERROR] ------ problem with reading file data ------"

            ret['data'] = data

    return ret
