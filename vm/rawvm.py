source = ''
ADDRESS_PREFIX = '#'
COMMENT_PREFIX = ';'

rom_elements = ["PC", "ZF", "SF"]

memory = {
    "RI": 0,
    "PC": 0,
    "ACC": 0,
    "EAX": 0,
    "ZF": 0,
    "SF": 0,
}

commands = [
    "ADD",
    "SUB",
    "MOV",
    "SHW", 
    "INC", 
    "DEC", 
    "HLT", 
    "END", 

    "CMP",
    "JMP",
    "JE",
    "JL",
    "JG",
    "JLE",
    "JGE",
    "JNE",
]

exlcuded_label_terms = [
    "",
    "HLT",
    '>',
]

error_messages = [
    "MISSING HALT",
    "REGISTER NOT FOUND AT LINE",
    "CODE NOT FOUND AT LINE",
    "FUNCTION NOT ENDED CORRECTLY",
    "OPERAND NOT FOUND AT LINE",
    "INVALID ARGUMENT SYNTAX AT LINE",
    "ACESSING ROM ADDRESS IS FORBIDDEN AT LINE",
    "OPERAND SYNTAX IS INVALID AT LINE",
    "FUNCTION CALLED IS NOT DEFINED AT LINE",
]

operations = [
    '+',
    '-',
    '*',
    '/',
    '//',
    '%',
]

output_buffer = []

import re
import utils
import memory as mem

def out(text, end="\n"):
    output_buffer.append(text + end)

def iterate():
    memory["PC"]+=1


def run(code:str):
    global source
    source = code.split("\n")
    code_len = len(source)

    function_define = False

    while (True):
        line = ["_"]
        if (memory["PC"] < code_len):
            line = utils.ignore_comments(source[memory["PC"]].strip().split(' '))
        else:
            utils.error_handler(error_messages[0]) if not function_define else utils.error_handler(error_messages[3])
            break

        if (mem.is_defining_func(line)):
            address = line[0] if len(line) == 2 else line[0][:-1]
            
            memory[address] = memory["PC"] +1
            function_define = True
            iterate()
            continue

        instruction = line[0].upper()

        if (instruction != ''):
            if (not function_define):
                match instruction:
                    case "ADD":
                        address = line[1][1:]
                        value = mem.resolve_value(line[2])

                        if (value == None):
                            utils.error_handler(error_messages[1], memory["PC"], " ".join(line))
                        else:
                            memory[address] += value

                    case "SUB":
                        address = mem.get_address(line[1])
                        value = mem.resolve_value(line[2])

                        if (value == None):
                            utils.error_handler(error_messages[1], memory["PC"], " ".join(line))
                        else:
                            memory[address] -= value

                    case "MOV":
                        address = mem.get_address(line[1])
                        expressions = " ".join(line[2:]).strip()

                        value = mem.resolve_value(expressions)
                        memory["RI"] = 0

                        if (value == None):
                            utils.error_handler(error_messages[1], memory["PC"], " ".join(line))
                        else:
                            if (address in rom_elements):
                                utils.error_handler(error_messages[6], memory["PC"], " ".join(line))
                            else:
                                memory[address] = value
                    
                    case "SHW":
                        content = line[1:] if (line[-1] not in exlcuded_label_terms) else line[1:-1]
                        value = utils.resolve_string(" ".join(content).strip()) 

                        if (value == "None" or value == None):
                            utils.error_handler(error_messages[1], memory["PC"], " ".join(line))
                        else:
                            if (line[-1] == '>'):
                                out(value)
                            else:
                                out(value, end="")

                    case "INC":
                        address = line[1][1:]
                        memory[address] += 1
                        
                    case "DEC":
                        address = line[1][1:]
                        memory[address] -= 1

                    case "JMP":
                        address = mem.get_address(line[1])
                        if (address in memory):
                            memory["PC"] = memory[address]
                            continue
                        else:
                            utils.error_handler(error_messages[8], memory["PC"], source[memory["PC"]])
    
                    case "CMP":
                        content = " ".join(line).split(maxsplit=1)
                        args = re.findall(r'\((.*?)\)', content[1])
                        if not args:
                            args = line[1:]

                        if (len(args) != 2):
                            utils.error_handler(error_messages[5], memory["PC"], source[memory["PC"]].strip(), 2, len(args))

                        val1 = mem.resolve_value(args[0])
                        val2 = mem.resolve_value(args[1])
                        memory["ZF"] = 1 if (val1 - val2 == 0) else 0
                        memory["SF"] = 1 if (val1 < val2) else 0
                        
                    case "JE":
                        utils.flag_is_valid(line)
                        address = mem.get_address(line[1])

                        if (memory["ZF"]):
                            memory["PC"] = memory[address]
                            continue

                    case "JL":
                        utils.flag_is_valid(line)
                        address = mem.get_address(line[1])

                        if (memory["SF"]):
                            memory["PC"] = memory[address]
                            continue

                    case "JG":
                        utils.flag_is_valid(line)
                        address = mem.get_address(line[1])

                        if (not memory["SF"] and not memory["ZF"]):
                            memory["PC"] = memory[address]
                            continue

                    case "JLE":
                        address = mem.get_address(line[1])
                        if (memory["SF"] or memory["ZF"]):
                            memory["PC"] = memory[address]
                            continue

                    case "JGE":
                        address = mem.get_address(line[1])
                        if not (memory["SF"]):
                            memory["PC"] = memory[address]
                            continue

                    case "JNE":
                        address = mem.get_address(line[1])
                        if not (memory["ZF"]):
                            memory["PC"] = memory[address]
                            continue

                    case "HLT":
                        print("".join(output_buffer))
                        break
    
                    case "}":
                        continue
                
                    case _:
                        utils.error_handler(error_messages[2], memory["PC"], " ".join(line))
                        break

        if (instruction == "}"):
            function_define = False
        iterate()