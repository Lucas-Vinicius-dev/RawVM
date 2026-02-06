import rawvm as vm
import utils

def get_address(token):
    return token[1:]

def resolve_operation(operand, operator=vm.memory["RI"]):
    if (type(operand) == str):
        if (operand.isdigit()):
            operand = int(operand)
        else :
            utils.error_handler(vm.error_messages[7], vm.memory["PC"], vm.source[vm.memory["PC"]].strip())

    match (operator):
        case "+":
            vm.memory["ACC"] += operand
        case "-":
            vm.memory["ACC"] -= operand
        case "*":
            vm.memory["ACC"] *= operand
        case "/":
            vm.memory["ACC"] /= operand
        case "//":
            vm.memory["ACC"] //= operand
        case "%":
            vm.memory["ACC"] %= operand
        case _:
            if (operator != 0):
                utils.error_handler(vm.error_messages[4], vm.memory["PC"], vm.source[vm.memory["PC"]].strip())
            else:
                vm.memory["ACC"] = operand


def resolve_value(token, associate=True):
    vm.memory["ACC"] = 0
    tokens = token.split(' ')

    for tk in tokens:
        if (len(tk) > 0):
            if (tk[0] == vm.ADDRESS_PREFIX):
                if (tk[1:] in vm.memory):
                    resolve_operation(vm.memory[tk[1:]], vm.memory["RI"])
            elif (tk in vm.operations):
                if (not associate):
                    return tk 
                vm.memory["RI"] = tk
            else:
                resolve_operation(tk, vm.memory["RI"])
    return vm.memory["ACC"]

def is_defining_func(line):
    return (line[-1] != '' and line[-1][-1] == '{' and (len(line) == 2 or len(line) == 1))