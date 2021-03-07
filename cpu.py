class Registers:
	def __init__(self, a=0, x=0, y=0, pc=0, flags=0):

		# Define Registers
		self.a = a
		self.x = x
		self.y = y
		self.pc = pc
		self.flags = flags

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
	def inc_pc(self):
		self.pc += 1

	def read_pc(self):
		return self.pc

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
		flag_def = {"C" : 0b00000001,
					"Z" : 0b00000010,
					"I" : 0b00000100,
					"D" : 0b00001000,

					"s" : 0b00010000,
					"b" : 0b00100000,
					"V" : 0b01000000,
					"N" : 0b10000000}

		self.flags = self.flags | flag_def[flag]

	def disable_flag(self, flag):
		flag_def = {"C" : 0b00000001,
					"Z" : 0b00000010,
					"I" : 0b00000100,
					"D" : 0b00001000,

					"s" : 0b00010000,
					"b" : 0b00100000,
					"V" : 0b01000000,
					"N" : 0b10000000}

		self.flags = self.flags & (~flag_def[flag])

	def read_flags(self):
		return self.flags





class CPU:
	def __init__(self, ROM = []):
		self.registers = Registers()
		self.ROM = ROM

		# Create RAM
		self.RAM_len = 256
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
						   10 : self.LDY
		}


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






	# Print CPU Info
	def print_info(self):
		print("\n\n-----------\n")
		print("REGISTERS")
		print(" A: ", self.registers.read_a())
		print("PC: ", self.registers.read_pc())

		print("\nMEMORY")
		for i in range(len(self.RAM)):
			print("{:02d} : {}".format(i, self.RAM[i]))



	# Running Code

	def run(self):
		self.ROM = program

		running = True
		while running:
			task = self.operations.get(self.ROM[self.registers.read_pc()], 
									   self.error)
			running = task()

			self.print_info()

			if not running:
				print("Program Stopped.")

			self.registers.inc_pc()







program = [1, 0x64, 2, 0x07, 3, 15, 0]

cpu = CPU(program)
cpu.run()