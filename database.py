database_path = "database.txt"

def save_input(value):
	file = open(database_path, "a+")
	file.write(str(value))
	file.close()

def save_result(value: str):
	file = open(database_path, "a")
	file.write(" / " + value)
	file.write("\n")
	file.close()

def read_all():
	file = open(database_path, "r")
	lines = file.readlines()
	results = []
	for i, line in enumerate(lines):
		results.append([])
		result = line.split(" / ")
		results[i] += result
		print(results[i])
	return results