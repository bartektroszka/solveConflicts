import random
import os

def is_nick(name):
    alphabet = 'abcdefghijklmnopqrstuvwxyz_0123456789'
    return all([letter in alphabet for letter in name])


def random_id():
    alphabet = 'abcdefghijklmnopqrstuvwxyz_0123456789'
    return ''.join([random.choice(alphabet) for _ in range(10)])


def run_command(command):
    print("RUNNING COMMAND")
    print(f"{command}: \033[31m{os.popen(command).read()}\033[m")