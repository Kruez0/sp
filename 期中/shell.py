import Program

while True:
		text = input('Program > ')
		result, error = Program.run('<stdin>', text)

		if error: print(error.as_string())
		else: print(result)