import os


def is_nick(name):
    alphabet = 'abcdefghijklmnopqrstuvwxyz_0123456789'
    return all([letter in alphabet for letter in name])


def update_tree(request_data):
    if not isinstance(request_data, dict):
        return "[ERROR] request.json is not a dictionary"

    if 'nick' not in request_data.keys():
        return "[ERROR] 'nick' key was not specified"

    if not is_nick(request_data['nick']):
        return "[ERROR] 'nick' value must consist only of digits, '_'  and low latin letter"

    if 'tree' not in request_data.keys():
        return "[ERROR] 'tree' key was not specified"

    file_path = os.path.abspath(os.getcwd())
    file_path = os.path.join(file_path, 'users_data')

    if not os.path.isdir(file_path):
        return "[ERROR] no 'users_data' directory in application directory"

    file_path = os.path.join(file_path, request_data['nick'])

    if not os.path.isdir(file_path):
        return f"[ERROR] No user called '{request_data['nick']}'"

    if request_data['tree']['label'] != request_data['nick']:
        return "[ERROR] Home folder name differs from nick of the user"

    def recurse_over_tree(current_path, tree):
        list_of_dirs = []
        list_of_files = []

        if os.path.isdir(current_path):
            for subdir, dirs, files in os.walk(current_path):
                # print(f"{current_path=}: {dirs = }, {files =}")

                list_of_dirs = [os.path.join(current_path, directory) for directory in dirs]
                list_of_files = [os.path.join(current_path, file) for file in files]
                break

        my_list_of_dirs = []
        my_list_of_files = []

        for element in tree['items']:
            new_path = os.path.join(current_path, element['label'])
            if 'items' in element.keys():
                my_list_of_dirs.append(new_path)
            else:
                my_list_of_files.append(new_path)

        for directory in list_of_dirs:
            if directory not in my_list_of_dirs:
                print(f"rm -r {directory} [ale nie wykonuję tej komendy, bo usuwanie niebezpieczne]")

        for file in list_of_files:
            if file not in my_list_of_files:
                print(f"rm {file}, [ale bez usuwania, bo safety]")

        for element in tree['items']:
            new_path = os.path.join(current_path, element['label'])
            if 'data' in element.keys():
                os.popen(f"echo '{element['data']}' > {new_path}")
            else:
                if not 'items' in element.keys():
                    print("[ERROR] Tree object has to have either items on data field!")

                if not os.path.isdir(new_path):
                    try:
                        os.mkdir(new_path)
                    except:
                        print("[TODO?] Problem with creating file")

                recurse_over_tree(new_path, element)

    recurse_over_tree(file_path, request_data['tree'])


def get_directory_tree(path, len_of_prefix):
    ret = {
        'label': path[len_of_prefix:],
        'parent': None
    }

    if os.path.isdir(path):
        ret['items'] = []
        for filename in os.listdir(path):
            if filename[0] == '.':
                continue
            full_filename = os.path.join(path, filename)

            if os.path.isdir(full_filename) or os.path.isfile(full_filename):
                ret['items'].append(get_directory_tree(full_filename, len(path) + 1))
                ret['items'][-1]['parent'] = path[len_of_prefix:]

    else:
        if not os.path.isfile(path):
            return f"Path '{path}' leads neither to a file nor to a directory!"

        with open(path, 'r') as f:
            try:
                data = f.read()
            except:
                data = "------ problem with reading file data ------"

            ret['data'] = data

    return ret


if __name__ == "__main__":
    print("name is equal to main ni")
