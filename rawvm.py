import os

PREFIX = '#'

memory = {
    "RI": 0,
    "PC": 0,
    "ACC": 0,
    "EAX": 0,
    "ZF": 0,
    "SF": 0,
}

commands = [
    "ADD", # Soma um número ou o conteúdo de um endereço
    "SUB", # Subtrai um número ou o conteúdo de um endereço para um endereço
    "MOV", # Seta o conteúdo de um endereço com um valor
    "SHW", # Mostra o resultado do valor de um endereço
    "INC", # Incrementa o conteúdo de um endereço em 1
    "DEC", # Reduz o conteúdo de um endereço em 1
    "HLT", # Para o programa
    "END", # Termina o escopo da função
    
    # Salvam o resultado do operador lógico em um endereço
    "AND", 
    "NAND",  
    "OR", 
    "NOR", 
    "NOT",
    "XOR",
    "XNOR",

    # Operações condicionais
    "CMP",
    "JMP",
    "EJ",
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
    "FUNCTION NOT ENDED CORRECTLY"
]


def error_handler(message, line='', line_content = ''):
    print("ERROR ||",message, line, "||" , line_content,  end='')
    

output_buffer = []

def out(text, end="\n"):
    output_buffer.append(text + end)

def interpret_content(prefix, content, _type):
    type_map = {
        "INT": int,
        "STR": str,
        "FLOAT": float,
        "BOOL": bool,
    }

    if (prefix == PREFIX):
        if (content[1:] in memory):
            return memory[content[1:]]
        return None
    return type_map[_type](content)

def iterate():
    memory["PC"]+=1


def get_address(token):
    return token[1:]

def resolve_value(token, _type="INT"):
    prefix = token[0]
    return interpret_content(prefix, token, _type)

def resolve_string(token):
    tokens = token.split(' ')
    message = []

    for tk in tokens:
        if (tk[0] == PREFIX): 
            if (tk[1:] in memory):
                message.append(str(memory[tk[1:]]))
                continue
            return "None"
        else:
            message.append(tk)
    return " ".join(message)

def run(code:str):
    code = code.split("\n")
    code_len = len(code)

    function_define = False

    while (True):
        line = ["_"]
        if (memory["PC"] < code_len):
            line = code[memory["PC"]].split(' ')
        else:
            error_handler(error_messages[0]) if not function_define else error_handler(error_messages[3])
            break
            

        if (len(line) == 1):
            definition = line[0]
            if (definition not in exlcuded_label_terms):
                match definition[-1]:
                    case ':':
                        memory[definition[:-1]] = memory["PC"] +1 
                        function_define = True
                        iterate()
                        continue

        instruction = line[0].upper()

        if (instruction != ''):
            if (not function_define):
                match instruction:
                    case "ADD":
                        address = line[1][1:]
                        value = resolve_value(line[2])

                        if (value == None):
                            error_handler(error_messages[1], memory["PC"], code[memory["PC"]])
                            break
                        else:
                            memory[address] += value

                    case "SUB":
                        address = get_address(line[1])
                        value = resolve_value(line[2])

                        if (value == None):
                            error_handler(error_messages[1], memory["PC"], code[memory["PC"]])
                            break
                        else:
                            memory[address] -= value

                    case "MOV":
                        address = get_address(line[1])
                        value = resolve_value(line[2])

                        if (value == None):
                            error_handler(error_messages[1], memory["PC"], code[memory["PC"]])
                            break
                        else:
                            memory[address] = value
                    
                    case "SHW":
                        content = line[1:] if (line[-1] not in exlcuded_label_terms) else line[1:-1]
                        prefix = content[0]
                        value = resolve_string(" ".join(content).strip()) 

                        if (value == None):
                            error_handler(error_messages[1], memory["PC"], code[memory["PC"]])
                            break
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
                        address = get_address(line[1])
                        memory["PC"] = memory[address]
                        continue

                    case "JE":
                        address = get_address(line[1])

                        if (memory["ZF"]):
                            memory["PC"] = memory[address]
                            continue

                    case "JL":
                        address = get_address(line[1])

                        if (memory["SF"]):
                            memory["PC"] = memory[address]
                            continue

                    case "CMP":
                        val1 = resolve_value(line[1])
                        val2 = resolve_value(line[2])
                        memory["ZF"] = 1 if (val1 - val2 == 0) else 0
                        memory["SF"] = 1 if (val1 < val2) else 0
                        
                    case "HLT":
                        print("".join(output_buffer))
                        break
                    case "END":
                        continue
                    case _:
                        error_handler(error_messages[2], memory["PC"], code[memory["PC"]])
                        break

        if (instruction == "END"):
            function_define = False
        iterate()