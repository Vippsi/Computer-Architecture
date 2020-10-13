"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.pc = 0
        self.ram = [0] * 256
        self.processing = False

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        if len(sys.argv) != 2:
            print("usage: cpu.py programname")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.strip()
                    if line == '' or line[0] == "#":
                        continue
                    
                    try:
                        str_value = line.split("#")[0]
                        value = int(str_value, base=2) #Need to specify the base for binary in this line int(value, base = 2)
                    except ValueError:
                        print(f"Invalid number: {str_value}")
                        sys.exit(1)

                    self.ram[address] = value
                    address += 1
        except FileNotFoundError:
            print(f"File not found: {sys.argv[1]}")
            sys.exit(2)


    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MULT":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.processing = True
        # self.trace()
        while self.processing:
            instruction = self.ram[self.pc] 
            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]


            if instruction ==   0b00000001:
                self.HLT()

            elif instruction == 0b10000010:
                self.LDI()
            
            elif instruction == 0b01000111:
                self.PRN()
            
            elif instruction == 0b10100010:  # MUL
                self.alu("MULT", operand_a, operand_b)
            
            else:
                print(f"Unknown instruction {instruction} at at {self.pc}")
                sys.exit(1)

            inst_len = (instruction >> 6) + 1
            self.pc += inst_len

    def HLT(self):
        self.processing = False

    def LDI(self):
        reg_num = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]

        self.reg[reg_num] = value
        # self.pc += 3

    def PRN(self):
        reg_num = self.ram[self.pc + 1]
        print(self.reg[reg_num])
        # self.pc += 2
    
    
        


