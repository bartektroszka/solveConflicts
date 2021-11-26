import os


# Some useless classes?
# class TreeElement:
#     def __init__(self, my_id, label, parent_id):
#         self.id = my_id
#         self.label = label
#         self.parent_id = parent_id
#
#
# class File(TreeElement):
#     def __init__(self, my_id, label, parent_id, data):
#         super().__init__(my_id, label, parent_id)
#         self.type = 'file'
#         self.data = data
#
#     def __repr__(self):
#         return f"Plik: {self.label}, Data: {self.data}"
#
#
# class Directory(TreeElement):
#     def __init__(self, my_id, label, parent_id, items):
#         super().__init__(my_id, label, parent_id)
#         self.type = 'dir'
#         self.items = items  # list of ids
#
#     def __repr__(self):
#         return f"Directory: {self.label}, Items: {self.items}"


def is_nick(name):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    digits = '0123456789'

    return all([letter in alphabet or letter in digits for letter in name])


def update_tree(request_data):
    if 'nick' not in request_data.keys():
        return ["'nick' value was not specified"]
    if not is_nick(request_data['nick']):
        return ["'nick' value must consist only of digits and low latin letter"]

    if 'tree' not in request_data.keys():
        return ["'tree' value was not specified"]

    ret_list = []

    file_path = os.path.abspath(os.getcwd())
    file_path = os.path.join(file_path, 'users_data')

    if not os.path.isdir(file_path):
        return "[internal error] no 'users_data' directory in application directory"

    file_path = os.path.join(file_path, request_data['nick'])

    if not os.path.isdir(file_path):
        try:
            os.mkdir(file_path)
        except:
            return "Problem with creating user login"

    file_path = os.path.join(file_path, request_data['tree'][0]['label'])
    if not os.path.isdir(file_path):
        try:
            os.mkdir(file_path)
        except:
            return "Unknown issue"

    def recurse_over_tree(current_path, tree):
        list_of_dirs = []
        list_of_files = []

        if os.path.isdir(current_path):
            for subdir, dirs, files in os.walk(current_path):
                list_of_dirs = [os.path.abspath(directory) for directory in dirs]
                list_of_files = [os.path.abspath(file) for file in files]
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
                    print("specification error - tree object has to have either items on data field!")

                if not os.path.isdir(new_path):
                    try:
                        os.mkdir(new_path)
                    except:
                        print("Problem with creating file")

                recurse_over_tree(new_path, element)

    recurse_over_tree(file_path, request_data['tree'][0])
    return ret_list


def get_directory_tree(path, len_of_prefix):
    ret = {
        'filename': path[len_of_prefix:],
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
