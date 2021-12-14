import random
import os

def is_nick(name):
    alphabet = 'abcdefghijklmnopqrstuvwxyz_0123456789'
    return all([letter in alphabet for letter in name])


# Functions for managing colors in output console
def red(string_to_color):
    return '\033[31m' + string_to_color + '\033[m'


def yellow(string_to_color):
    return '\033[33m' + string_to_color + '\033[m'


def green(string_to_color):
    return '\033[32m' + string_to_color + '\033[m'


def random_id():
    alphabet = 'abcdefghijklmnopqrstuvwxyz_0123456789'
    return ''.join([random.choice(alphabet) for _ in range(10)])


def run_command(command, debug=False):
    if debug:
        print("Command to run: ", command)
    return os.popen(command).read()