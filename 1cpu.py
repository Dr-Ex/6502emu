class Registers:
	def __init__(self, a=0, pc=0):

		# Accumulator
		self.a = a

		# Program Counter
		self.pc = pc

	def set_a(self, value):
		self.a = value

	def read_a(self):
		return self.a

	def step_pc(self, iterations = 1):
		self.pc += iterations

	def read_pc(self):
		return self.pc


class CPU:
	def __init__(self, ROM = []):
		self.registers = Registers()
		self.ROM = ROM
		self.RAM_len = 16
		self.RAM = [0 for x in range(self.RAM_len)]
		

		# Operations Map
		self.operations = {0 : self.BRK,
						   1 : self.LDA,
						   2 : self.ADC,
						   3 : self.STA
		}


	# Operations

	def BRK(self):
		return False

	def LDA(self):
		self.registers.step_pc()

		# Store the value at the current ROM address into A register
		self.registers.set_a(self.ROM[self.registers.read_pc()])
		return True

	def ADC(self):
		self.registers.step_pc()
		
		# Add the value in the current ROM address to the A register
		self.registers.set_a(self.registers.read_a() + 
							 self.ROM[self.registers.read_pc()])
		return True

	def STA(self):
		self.registers.step_pc()

		# If the memory location to be stored is greater than the 
		# RAM size, print and throw error
		if self.ROM[self.registers.read_pc()] > self.RAM_len:
			print("ERROR ADC: Address out of bounds.")
			return False

		# Set specified RAM address to the value in the A register
		self.RAM[self.ROM[self.registers.read_pc()]] = self.registers.read_a()
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
									   "ERROR RUN: Invalid Operation")
			running = task()

			self.print_info()

			if not running:
				print("Program Stopped.")

			self.registers.step_pc()







program = [1, 0x64, 2, 0x07, 3, 15, 0]

cpu = CPU(program)
cpu.run()