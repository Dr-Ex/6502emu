# Created by Henry Nicholson
# 07 - 03 - 2021

class Registers:
	def __init__(self, a=0, x=0, y=0, pc=0, sp=639, flags=0):

		# Define Registers
		self.a = a
		self.x = x
		self.y = y
		self.pc = pc
		self.sp = sp
		self.flags = flags

		self.flag_def = {"C" : 0b00000001,
						 "Z" : 0b00000010,
						 "I" : 0b00000100,
						 "D" : 0b00001000,

						 "s" : 0b00010000,
						 "b" : 0b00100000,
						 "V" : 0b01000000,
						 "N" : 0b10000000}

	# A Register Operations
	def set_a(self, value):
		self.a = value

	def read_a(self):
		return self.a


	# X Register Operations
	def set_x(self, value):
		self.x = value

	def inc_x(self):
		self.x += 1

	def read_x(self):
		return self.x


	# Y Register Operations
	def set_y(self, value):
		self.y = value

	def read_y(self):
		return self.y


	# Program Counter Operations
	def inc_pc(self, step = 1):
		self.pc += step

	def set_pc(self, value):
		self.pc = value

	def read_pc(self):
		return self.pc

	# Stack Pointer Operations
	def set_sp(self, value):
		self.sp = value

	def read_sp(self):
		return self.sp

	# Status Flags
	#
	# 7  bit  0
	# ---- ----
	# NVbs DIZC
	# |||| ||||
	# |||| |||+- Carry
	# |||| ||+-- Zero - Result of CMY/CMP etc.
	# |||| |+--- Interrupt Disable
	# |||| +---- Decimal
	# ||++------ No CPU effect, see: the B flag
	# |+-------- Overflow
	# +--------- Negative

	def set_flag(self, flag):
		self.flags = self.flags | self.flag_def[flag]

	def disable_flag(self, flag):
		self.flags = self.flags & (~self.flag_def[flag])

	def get_flag(self, flag):
		if (self.flags & self.flag_def[flag]) > 0:
			return True
		else:
			return False

	def read_flags(self):
		return self.flags





class CPU:
	def __init__(self, ROM = []):
		self.registers = Registers()
		self.ROM = ROM

		# Create RAM
		self.RAM_len = 640
		# RESERVE location 128-255 for ASCII text to print
		#self.RAM_ASCII_reserve = 128
		self.RAM = [0 for x in range(self.RAM_len)]
		

		# Operations Map
		self.operations = {0 : self.BRK,
						   1 : self.LDA,
						   2 : self.ADC,
						   3 : self.STA,
						   4 : self.LDX,
						   5 : self.INX,
						   6 : self.CMY,
						   7 : self.BNE,
						   8 : self.STA_X,
						   9 : self.DEY,
						   10 : self.LDY,
						   11 : self.JSR,
						   12 : self.RTS}


	# Operations

	def error(self):
		print("ERROR RUN: Invalid Operation")
		return False

	def BRK(self):
		return False

	def LDA(self):
		self.registers.inc_pc()

		# Store the value at the current ROM address into A register
		self.registers.set_a(self.ROM[self.registers.read_pc()])
		return True

	def ADC(self):
		self.registers.inc_pc()
		
		# Add the value in the current ROM address to the A register
		self.registers.set_a(self.registers.read_a() + 
							 self.ROM[self.registers.read_pc()])
		return True

	def STA(self):
		self.registers.inc_pc()

		# If the memory location to be stored is greater than the 
		# RAM size, print and throw error
		if self.ROM[self.registers.read_pc()] > self.RAM_len:
			print("ERROR ADC: Address out of bounds.")
			return False

		# Set specified RAM address to the value in the A register
		self.RAM[self.ROM[self.registers.read_pc()]] = self.registers.read_a()
		return True


	def LDX(self):
		self.registers.inc_pc()

		# Store the value at the current ROM address into X register
		self.registers.set_x(self.ROM[self.registers.read_pc()])
		return True

	def INX(self):
		self.registers.inc_x()
		return True

	def CMY(self):
		self.registers.inc_pc()

		if self.ROM[self.registers.read_pc()] == self.registers.read_y():
			self.registers.set_flag("Z")
		else:
			self.registers.disable_flag("Z")

		return True

	def BNE(self):
		self.registers.inc_x()
		
		if not self.check_flag("Z"):
			self.registers.inc_x(self.ROM[self.registers.read_pc()])
		return True

	def STA_X(self):
		self.RAM[self.registers.read_x()] = self.registers.read_a()
		return True

	def DEY(self):
		self.registers.set_y(self.registers.read_y() - 1)
		return True

	def LDY(self):
		self.registers.inc_pc()

		self.registers.set_y(self.RAM[self.registers.read_pc()])

	def JSR(self):
		self.registers.inc_pc()

		# Add current pc to the stack
		self.RAM[self.registers.read_sp()] = self.registers.read_pc()

		# Subtract 1 from sp
		self.registers.set_sp(self.registers.read_sp() - 1)

		# Set PC to the current value in ROM
		self.registers.set_pc(self.ROM[self.registers.read_pc()] - 1)

		return True

	def RTS(self):
		self.registers.set_sp(self.registers.read_sp() + 1)

		self.registers.set_pc(self.RAM[self.registers.read_sp() + 1])

		return True





	# Print CPU Info
	def print_registers(self):
		print("\n\n-----------\n")
		print("REGISTERS")
		print(" A: ", self.registers.read_a())
		print(" X: ", self.registers.read_x())
		print(" Y: ", self.registers.read_y())
		print("PC: ", self.registers.read_pc())
		print("FL: ", self.registers.read_flags())

	def print_memory(self):
		print("\nMEMORY")
		for i in range(len(self.RAM)):
			if self.RAM[i] > 0:
				print("{:02d} : {}".format(i, self.RAM[i]))

	def print_ASCII(self):
		print(''.join(chr(i) for i in self.RAM[128:]))



	# Running Code

	def run(self):
		running = True
		while running:
			task = self.operations.get(self.ROM[self.registers.read_pc()], 
									   self.error)

			print("TASK: ", task)
			running = task()

			self.print_registers()
			self.print_memory()


			if not running:
				self.print_ASCII()
				print("Program Stopped.")


			self.registers.inc_pc()







program1 = [1, 0x64, 2, 0x07, 3, 15, 0]

program2 = [4, 128, 1, 0x77, 8, 5, 1, 0x68, 8, 5, 1, 0x6F, 8, 5, 1, 0x20, 8, 5, 1, 0x6c, 8, 5, 1, 0x65, 8, 5, 1, 0x74, 8, 5, 1, 0x20, 8, 5, 1, 0x74, 8, 5, 1, 0x68, 8, 5, 1, 0x65, 8, 5, 1, 0x20, 8, 5, 1, 0x64, 8, 5, 1, 0x6F, 8, 5, 1, 0x67, 8, 5, 1, 0x73, 8, 5, 1, 0x20, 8, 5, 1, 0x6F, 8, 5, 1, 0x75, 8, 5, 1, 0x74, 8, 5, 1, 0x20, 8, 5, 10, 3, 1, 0x77, 8, 5, 1, 0x68, 8, 5, 1, 0x6F, 8, 5, 1, 0x20, 8, 5, 9, 6, 0, 7, -20, 0]

cpu = CPU(program2)
cpu.run()
