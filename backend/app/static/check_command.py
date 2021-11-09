# function for checkign whether used provided command is valid git command
import re
splitter = re.compile(r" |\t")

def valid_command(line):
    words = splitter.split(line)
    words = [word for word in words if len(word) > 0]
    print("WORDS: ", words)

    return len(words) > 0 and words[0] == 'git'

if __name__ == '__main__':
    command_to_check = "\tgit\t\thelloe    fjnds "
    print("GOOD " if valid_command(command_to_check) else "BAD")