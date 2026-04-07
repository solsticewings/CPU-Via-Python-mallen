"""
Catamount Processing Unit
A toy 16-bit Harvard architecture CPU.

CS 2210 Computer Organization
Clayton Cafiero <cbcafier@uvm.edu>

STARTER CODE
"""

from alu import Alu
from constants import STACK_TOP
from instruction_set import Instruction
from memory import DataMemory, InstructionMemory
from register_file import RegisterFile


class Cpu:
    """
    Catamount Processing Unit
    """

    def __init__(self, *, alu, regs, d_mem, i_mem):
        """
        Constructor
        """
        self._i_mem = i_mem
        self._d_mem = d_mem
        self._regs = regs
        self._alu = alu
        self._pc = 0  # program counter
        self._ir = 0  # instruction register
        self._sp = STACK_TOP  # stack pointer
        self._decoded = Instruction()
        self._halt = False

    @property
    def running(self):
        return not self._halt

    @property
    def pc(self):
        return self._pc

    @property
    def sp(self):
        return self._sp

    @property
    def ir(self):
        return self._ir

    @property
    def decoded(self):
        return self._decoded

    def get_reg(self, r):
        """
        Public accessor (getter) for single register value.
        """
        return self._regs.execute(ra=r)[0]

    def tick(self):
        """
        Fetch-decode-execute
        Implementation incomplete.
        """
        if not self._halt:
            self._fetch()
            self._decode()

            # execute...
            match self._decoded.mnem:
                case "LOADI":
                    rd = self._decoded.rd
                    data = self._decoded.imm & 0xFF
                    self._regs.execute(rd=rd, data=data, write_enable=True)
                    # complete implementation here?
                case "LUI":
                    # TODO Refactor for future semester(s) if any.
                    # Cheating for compatibility with released ALU tests
                    # and starter code. Leave as-is for 2025 Fall.
                    rd = self._decoded.rd
                    imm = self._decoded.imm & 0xFF
                    upper = imm << 8
                    lower, _ = self._regs.execute(ra=rd)
                    lower &= 0x00FF  # clear upper bits
                    data = upper | lower
                    self._regs.execute(rd=rd, data=data, write_enable=True)
                case "LOAD":
                    rd = self._decoded.rd
                    ra = self._decoded.ra
                    addr = self._decoded.addr
                    # Get base address from register
                    base_addr, _ = self._regs.execute(ra=ra, write_enable=False)
                    # Calculate offset
                    offset = base_addr + self.sext(addr, 16)
                    data = self._d_mem.read(offset)
                    self._regs.execute(rd=rd, data=data, write_enable=True)
                    # complete implementation here?
                case "STORE":
                    ra = self._decoded.ra
                    rb = self._decoded.rb
                    addr = self._decoded.addr
                    data, offset = self._regs.execute(ra=ra, rb=rb, write_enable=False)
                    offset += self.sext(addr, 16) # calculate the effective address (added self for test)
                    self._d_mem.write_enable(True)
                    self._d_mem.write(offset, data)
                    self._d_mem.write_enable(False)
                    # complete implementation here?
                case "ADDI":
                    ra = self._decoded.ra
                    rd = self._decoded.rd
                    imm = self._decoded.imm
                    ra_value , _ = self._regs.execute(ra=ra, write_enable=False)
                    data = ra_value + self.sext(imm, 6)
                    self._regs.execute(rd=rd, data=data, write_enable=True)
                    # complete implementation here?
                case "ADD":
                    ra = self._decoded.ra
                    rb = self._decoded.rb
                    rd = self._decoded.rd
                    a, b = self._regs.execute(ra=ra, rb=rb, write_enable=False)
                    self._alu.set_op("ADD")
                    data = self._alu.execute(a, b)
                    self._regs.execute(rd=rd, data=data, write_enable=True)
                    # complete implementation here?
                case "SUB":
                    ra = self._decoded.ra
                    rb = self._decoded.rb
                    rd = self._decoded.rd
                    a, b = self._regs.execute(ra=ra, rb=rb, write_enable=False)
                    self._alu.set_op("SUB")
                    data = self._alu.execute(a, b)
                    self._regs.execute(rd=rd, data=data, write_enable=True)
                    # complete implementation here?
                case "AND":
                    ra = self._decoded.ra
                    rb = self._decoded.rb
                    rd = self._decoded.rd
                    a, b = self._regs.execute(ra=ra, rb=rb, write_enable=False)
                    self._alu.set_op("AND")
                    data = self._alu.execute(a, b)
                    self._regs.execute(rd=rd, data=data, write_enable=True)
                    # complete implementation here
                case "OR":
                    ra = self._decoded.ra
                    rb = self._decoded.rb
                    rd = self._decoded.rd
                    a, b = self._regs.execute(ra=ra, rb=rb, write_enable=False)
                    self._alu.set_op("OR")
                    data = self._alu.execute(a, b)
                    self._regs.execute(rd=rd, data=data, write_enable=True)
                case "SHFT":
                    self._alu.set_op("SHFT")
                    rd = self._decoded.rd
                    ra = self._decoded.ra
                    rb = self._decoded.rb
                    op_a, op_b = self._regs.execute(ra=ra, rb=rb, write_enable=False)
                    result = self._alu.execute(op_a, op_b)
                    self._regs.execute(rd=rd, data=result, write_enable=True)
                case "BEQ":
                    if self._alu.zero:
                        imm = self._decoded.imm
                        offset = self.sext(imm, 8)
                        self._pc += offset  # take branch
                case "BNE":
                    if not(self._alu.zero):
                        imm = self._decoded.imm
                        offset = self.sext(imm, 8)
                        self._pc += offset # take branch
                    # complete implementation here?
                case "B":
                    offset = self.sext(self._decoded.imm, 8)
                    self._pc += offset # take branch
                    # complete implementation here?
                case "CALL":
                    self._sp -= 1  # grow stack downward
                    # PC is incremented immediately upon fetch so already
                    # pointing to next instruction, which is return address.
                    ret_addr = self._pc  # explicit
                    self._d_mem.write_enable(True)
                    # push return address...
                    self._d_mem.write(self._sp, ret_addr, from_stack=True)
                    offset = self._decoded.imm
                    self._pc += self.sext(offset, 8)  # jump to target
                case "RET":
                    # Get return address from memory via SP
                    ret_addr = self._d_mem.read(self._sp)
                    # Increment SP
                    self._sp += 1
                    # Update PC
                    self._pc = ret_addr
                    # complete implementation here?
                case "HALT":
                    self._halt = True
                    # complete implementation here?
                case _:  # default
                    raise ValueError(
                        "Unknown mnemonic: " + str(self._decoded) + "\n" + str(self._ir)
                    )

            return True
        return False

    def _decode(self):
        """
        We're effectively delegating decoding to the Instruction class.
        """
        self._decoded = Instruction(raw=self._ir)

    def _fetch(self):
        # use address in program counter to fetch the next instruction from memory
        # and store the fetched instruction in the instruction register
        self._ir = self._i_mem.read(self._pc)
        # increment the program counter
        self._pc += 1
        # complete implementation here?

    def load_program(self, prog):
        self._i_mem.load_program(prog)
    
    @staticmethod
    def sext(value, bits=16):
          mask = (1 << bits) - 1
          value &= mask
          sign_bit = 1 << (bits - 1)
          return (value ^ sign_bit) - sign_bit


# Helper function
def make_cpu(prog=None):
    alu = Alu()
    d_mem = DataMemory()
    i_mem = InstructionMemory()
    if prog:
        i_mem.load_program(prog)
    regs = RegisterFile()
    return Cpu(alu=alu, d_mem=d_mem, i_mem=i_mem, regs=regs)
