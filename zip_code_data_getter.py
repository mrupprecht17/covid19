import json
import datetime
import numpy as np

def zip_code_data(zip_code, race=None, gender=None):
	lag = 1
	roll = 7

	directory = "C:\\Users\\Michael\\OneDrive - California Institute of Technology\\Documents\\musings, et cetera\\COVID-19\\IL data\\"
	cases = []
	tests = []

	end_date = datetime.datetime.today() - datetime.timedelta(days=lag)
	iter_date = end_date - datetime.timedelta(days=roll)
	while iter_date <= end_date:
		filename = f"{directory}COVIDZip_{iter_date.strftime('%Y.%m.%d')}.json"
		_d = json.load(open(filename, "r"))
		
		for d in _d["zip_values"]:
			if d["zip"] == zip_code:
				break

		day_cases = d["confirmed_cases"]
		day_tests = d["total_tested"]

		if race:
			for r in d["demographics"]["race"]:
				if r["description"] == race:
					day_cases = r["count"]
					day_tests = r["tested"]
					break
		elif gender:
			for g in d["demographics"]["gender"]:
				if g["description"] == gender:
					day_cases = g["count"]
					day_tests = g["tested"]
					break

		cases.append(day_cases)
		tests.append(day_tests)

		iter_date += datetime.timedelta(days=1)

	cases = np.array(cases)
	tests = np.array(tests)

	new_cases = cases[1:] - cases[:-1]
	new_tests = tests[1:] - tests[:-1]
	positivity_rate = new_cases / new_tests

	return positivity_rate, np.mean(positivity_rate), sum(new_cases) / sum(new_tests)

if __name__ == '__main__':
	zip_codes = [
		# west
		60631,
		60656,
		60706,
		60634,

		# north
		60714,
		60053,
		60077,
		60076,
		60203,
		60712,
		60646,

		# ^ less urban
		# my zip code
		60630,
		# v more urban

		# south/east
		60641,
		60645,
		60659,
		60625,
		60618,

		# south side
		60636,
		60629,
		60621,
		60620,
		60619
	]
	zip_codes = map(str, zip_codes)

	for zip_code in zip_codes:
		arr, averaged, average = zip_code_data(zip_code)
		arr_white, averaged_white, average_white = zip_code_data(zip_code, race="White")
		print(zip_code, "\t", round(average * 100, 1), "\t", round(average_white * 100, 1))
