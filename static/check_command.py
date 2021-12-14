# function for checking whether used provided command is valid git command
# TODO writing a function that will accurate tell if the command to run for user is valid
import re

splitter = re.compile(r" |\t")


def valid_command(line):
    words = splitter.split(line)
    words = [word for word in words if len(word) > 0]
    print("WORDS: ", words)

    return len(words) > 0 and words[0] == 'git' and any(['|' in word for word in words])
