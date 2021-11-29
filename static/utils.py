import random


def is_nick(name):
    alphabet = 'abcdefghijklmnopqrstuvwxyz_0123456789'
    return all([letter in alphabet for letter in name])


def random_id():
    alphabet = 'abcdefghijklmnopqrstuvwxyz_0123456789'
    return ''.join([random.choice(alphabet) for _ in range(10)])
