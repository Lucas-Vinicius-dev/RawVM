*(The technical manual)*

```markdown
# RAW Instruction Set Architecture (v1.0.09999)

## Architecture & Memory

* **Addressing:** RAW uses a string-based memory map.
* **Variables:** Identified by the `#` prefix (e.g., `#counter`). There is no theoretical limit to the number of variables.
* **Flags:** The processor maintains two internal flags for conditional operations:
    * `ZF` (Zero Flag): Set when a result is zero (used for equality).
    * `SF` (Sign Flag): Set when a result is negative (used for comparison).

## Instruction Set (Opcodes)

The architecture consists of exactly 16 instructions, divided into **General Operations** and **Control Flow**.

### General Instructions

| Opcode | Arguments | Description | Example |
| :--- | :--- | :--- | :--- |
| **MOV** | `#var` `val` | Moves a value (or expression result) into a variable. | `mov #x 10` |
| **ADD** | `#var` `val` | Adds a value to the variable. | `add #x 5` |
| **SUB** | `#var` `val` | Subtracts a value from the variable. | `sub #x 2` |
| **INC** | `#var` | Increments the variable by 1. | `inc #i` |
| **DEC** | `#var` | Decrements the variable by 1. | `dec #i` |
| **SHW** | `val/text` | Outputs text or variable value to the console.(You can also combine text with memory address in the same instruction). It is also possible to use `>` at the end to skip to next line | `shw Value: #x >` |
| **IN** | `#var` `msg` | Prompts user input and stores it in `#var`. | `in #age Age: ` |
| **HLT** | - | Halts the VM execution. | `hlt` |

*(Note: The `MOV` command supports simple arithmetic expressions like `mov #c #a + #b`)*

### Control Flow (Branching)

Conditional jumps rely on the state of flags set by the last `CMP` instruction.

| Opcode | Condition | Logic | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| **CMP** | - | `A - B` | Compares two values and updates Flags. | `cmp (#x + 4) (#y * 2)` |
| **JMP** | - | - | Unconditional Jump. |
| **JE** | `==` | `ZF=1` | Jump to function address if Equal. | `je #main` | 
| **JNE** | `!=` | `ZF=0` | Jump to function address if Not Equal. | `jne #main` |
| **JG** | `>` | `SF=0, ZF=0`| Jump to function address if Greater. | `jg #main` |
| **JGE** | `>=` | `SF=0` | Jump to function address if Greater or Equal. | `jge #main` |
| **JL** | `<` | `SF=1` | Jump to function address if Less. | `jl #main` |
| **JLE** | `<=` | `SF=1, ZF=1`| Jump to function address if Less or Equal. | `jle #main` |

*(Note: You Just need to use parenthesis when you have an expression to evaluate, otherwhise, `cmp #x #y` would work normally)*

## Syntax Guide

### Labels and Blocks
RAW supports defining labels using braces `{ }` to improve readability and scope visualization, although they function as standard Assembly labels.
```
```
main {
    shw Hello World
    hlt
}

jmp #main