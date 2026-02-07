## RawVM
RawVM is a custom-built, Turing-complete Process Virtual Machine designed to explore the fundamentals of computing architecture. It runs on a unique 16-instruction ISA (Instruction Set Architecture) that bridges the gap between the raw power of Assembly and the developer experience of modern languages.

While traditional Assembly requires managing memory addresses and complex registers, RAW introduces a "High-Level Assembly" approach:

Named Variables (#score, #counter) instead of raw memory addresses.

Scoped Blocks (main { ... }) for visual organization.

Hybrid Syntax that remains close to the metal but easy to read.

It is the perfect playground for understanding how computers think, how stacks/registers work, and how logical flows are constructed at the lowest level.

## Key Features
*-> 16-Instruction Architecture: A minimalist, 4-bit design.*

*-> Dynamic Memory: No hard limit on registers; allocate variables on the fly.*

*-> Smart I/O: Built-in output buffering and interactive input handling.*

*-> Logic Engine: Complete set of flags (ZF, SF) and conditional jumps (JE, JL, JGE...) for complex algorithms.*

*-> Editor Support: Custom syntax highlighting for VS Code.*

## Installation

#### To use RawVM, you simply need to clone the repository. The project is written in pure Python (3.10+ recommended).

### Setting up
Clone the Repository

`git clone https://github.com/Lucas-Vinicius-dev/RawVM`

Enter in the directory

`cd vm`

### Running a program
You can execute .raw files directly using the Python interpreter.

`python rawrunner.py <path_to_file.raw>`

## Vs Code Syntax Highlight for Raw
Manual Installation:

##### Locate the folder rawlang-highlight inside this repository.
Move or copy that entire folder into your VS Code extensions directory:

`Windows: %USERPROFILE%\.vscode\extensions`

`Mac/Linux: ~/.vscode/extensions`

##### Restart VS Code.

*Open any .raw file, and the syntax highlighting will be active automatically.*
<br>

*Obs: You can always skip the installation process by installing the executable in RELEASES area.*

## Example
```
; FIBONACCI IN RAW VM

mov #a 0
mov #b 1
mov #c 0
in #iter How many numbers to generate: 

main {
    cmp #iter 0
    je #end

    shw #c | 
    
    ; Arithmetic operations
    mov #c #a + #b
    mov #a #b
    mov #b #c
    
    dec #iter
    jmp #main
}

end {
    hlt 
}

jmp #main
```

## Architecture Overview
For a detailed breakdown of all 16 opcodes and how the flags work, please refer to the [ISA Documentation](https://github.com/Lucas-Vinicius-dev/RawVM/tree/main/rawlang-highlight)

#### Quick Opcode Overview
```
MOV, ADD, SUB, INC | CMP, JMP, JE, JNE
DEC, SHW, IN,  HLT | JG,  JGE, JL, JLE
```
