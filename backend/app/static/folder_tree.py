import os


class TreeElement:
    def __init__(self, my_id, label, parent_id):
        self.id = my_id
        self.label = label
        self.parent_id = parent_id


class File(TreeElement):
    def __init__(self, my_id, label, parent_id, data):
        super().__init__(my_id, label, parent_id)
        self.type = 'file'
        self.data = data


class Directory(TreeElement):
    def __init__(self, my_id, label, parent_id, items):
        super().__init__(my_id, label, parent_id)
        self.type = 'dir'
        self.items = items  # list of ids


def is_nick(name):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    digits = '0123456789'

    return all([letter in alphabet or letter in digits for letter in name])


def list_of_commands_to_update_tree(request_data):
    if 'nick' not in request_data.keys():
        return ["'nick' value was not specified"]
    if not is_nick(request_data['nick']):
        return ["'nick' value must consist only of digits and low latin letter"]

    if 'tree' not in request_data.keys():
        return ["'tree' value was not specified"]

    my_dict = {}
    for element in request_data['tree']:
        my_id = element['id']
        label = element['label']
        parent_id = element['parentId']

        if 'items' in element.keys():
            # this element is a directory
            items = []
            for item in element['items']:
                items.append(item['id'])
            assert (my_id not in my_dict.keys())
            my_dict[my_id] = Directory(my_id, label, parent_id, items)
        else:
            # this element is a file
            data = element['data']
            assert (my_id not in my_dict.keys())
            my_dict[my_id] = File(my_id, label, parent_id, data)

    file_path = os.path.abspath(os.getcwd())
    file_path = os.path.join(file_path, 'users_data')
    assert (os.path.isdir(file_path))

    ret_list = []

    # ascending to initial directory
    root_id = -1
    for key, file in my_dict.items():
        if file.parent_id:
            assert (root_id == -1)
            root_id = file.id
            file_path = os.path.join(file_path, file.label)

            if not os.path.isfile(file_path):
                ret_list.append(f"mkdir {file_path}")

    def recurse_over_tree(current_path, current_id):
        list_of_dirs = []
        list_of_files = []

        if os.path.isdir(current_path):
            for subdir, dirs, files in os.walk(current_path):
                list_of_dirs = [os.path.abspath(directory) for directory in dirs]
                list_of_files = [os.path.abspath(file) for file in files]
                break

        my_list_of_dirs = []
        my_list_of_files = []

        for item in my_dict[current_id].items:
            new_path = os.path.join(current_path, item.label)
            if item.type == 'file':
                my_list_of_files.append(new_path)
            else:
                assert (item.type == 'dir')
                my_list_of_dirs.append(new_path)

        for directory in list_of_dirs:
            if directory not in my_list_of_dirs:
                ret_list.append(f"rm -r {directory}")

        for file in list_of_files:
            if file not in my_list_of_files:
                ret_list.append(f"rm {file}")

        for item in my_dict[current_id].items:
            new_path = os.path.join(current_path, item.label)
            if item.type == 'file':
                # if os.path.isdir(new_path): # TODO is this done before?
                #     ret_list.append(f"rm -r {new_path}")
                ret_list.append(f"echo {item.data} > {new_path}")
            else:
                assert (item.type == 'dir')
                if not os.path.isdir(new_path):
                    ret_list.append(f"mkdir {new_path}")
                recurse_over_tree(new_path, item.id)

    recurse_over_tree(file_path, root_id)

    return ret_list


if __name__ == "__main__":
    print("HELLO")

    my_dict = {
        "nick": "marcin",
        "tree": []
    }

    commands = list_of_commands_to_update_tree(my_dict)
    print("Finished")
