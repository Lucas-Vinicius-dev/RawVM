import rawvm as vm
import sys

def ignore_comments(line):
    for idx, element in enumerate(line):
        if (element != '' and element[0] == vm.COMMENT_PREFIX):
            return line[:idx] if line[:idx] != [] else ['']
    return line

def error_handler(message, line='', line_content = '', expected='', got=''):
    line += 1 if line != '' else ''
    if (expected != '' and got != ''):
        print(f"ERROR || " + message + " " + str(line) + " || " + line_content + " || " + "Expected args= " + str(expected) + " || " + "Got= " + str(got))
    else:
        print(f"ERROR || " + message + " " + str(line) + " || " + line_content)
    sys.exit()

def flag_is_valid(line):
    if (len(line) > 2):
        error_handler(vm.error_messages[5], vm.memory["PC"], " ".join(line), 1, len(line)-1)

def resolve_string(token):
    tokens = token.split(' ')
    message = []

    for tk in tokens:
        if (len(tk) > 0 and tk[0] == vm.ADDRESS_PREFIX):
            if (tk[1:] in vm.memory):
                message.append(str(vm.memory[tk[1:]]))
                continue
            return "None"
        else:
            message.append(tk)
    return " ".join(message)