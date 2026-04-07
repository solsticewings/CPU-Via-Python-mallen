"""
Driver code for running assembly code and inspecting registers and memory.

CS 2210 Computer Organization
Clayton Cafiero <cbcafier@uvm.edu>
"""

import argparse
import sys

from assembler import assemble
from cpu import make_cpu

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="specify input file", type=str)
    parser.add_argument("--steps", help="limit number of steps", type=int)
    args = parser.parse_args()

    asm = ""
    ask = True
    if args.input:
        ask = False
        asm = args.input

    while True:
        if ask:
            asm = input("Enter name of assembly code file (in ./asm directory): ")
            if asm.lower() == "q":
                print("Goodbye!")
                sys.exit(0)
        asm = "./asm/" + asm
        ask = True
        try:
            with open(asm, "r") as fh:
                code = fh.readlines()
            break
        except FileNotFoundError:
            print(f"`{asm}` not found. Please try another filename or `q` to quit.")
        except IOError:
            print("Unable to read from device. Aborting.")
            sys.exit(1)
        except UnicodeDecodeError:
            print("Unable to decode as UTF-8. Please check file. Aborting.")
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Aborting.")
            sys.exit(1)

    print()
    prog = assemble(code)

    c = make_cpu(prog)

    if args.steps:
        print(f"Limiting to {args.steps} steps.")
        count = 0
        while c.running:
            c.tick()
            print(hex(c.pc))
            print(c.decoded)
            count += 1
            if count == args.steps:
                c._halt = True  # Yeah, cheating a little here. I know.
        print()
    else:
        while c.running:
            c.tick()

    print("Registers:")
    print(c._regs)  # Cheating a little here, too. I know.
    print()

    print("Memory:")
    for line in c._d_mem.hexdump():  # Cheating a little here, too. I know.
        if not line.endswith("0000 0000 0000 0000 0000 0000 0000 0000"):
            print(line)
    print()
