database_path = "database.txt"

def save_input(value, pipe_engaged, emergency_pipe_engaged, date):
	file = open(database_path, "a+")
	file.write((str(date).split(".")[0]) + " / " + str(value))
	if pipe_engaged:
		if emergency_pipe_engaged:
			file.write(" / Emergency pipe engaged")
		else:
			file.write(" / Water pipe engaged")
	else:
		file.write(" / None")
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
		result = line.split(" / ")
		results.append(result)

		print(results[i])
	return results