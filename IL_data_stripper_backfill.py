import json
import os

result = {
	"Illinois": {},
	"Cook": {},
	"Chicago": {},
	"60630": {}
}
dates = []

directory = "C:\\Users\\Michael\\OneDrive - California Institute of Technology\\Documents\\musings, et cetera\\COVID-19\\IL data\\"
filename = f"{directory}COVIDHistoricalTestResults_2020.07.04.json"
_d = json.load(open(filename, "r"))
for d in _d["historical_county"]["values"]:
	try:
		month, day, year = d["testDate"].split("/")
	except KeyError:
		month, day, year = d["testdate"].split("/") # because i guess they somehow mistyped july 3rd and nothing else (they corrected this on the 7th)

	if len(month) == 1: # shouldn't happen bc i'm only doing march through july but still good practice
		month = "0" + month
	if len(day) == 1: # shouldn't happen bc it's 0-padded, but still good practice
		day = "0" + day
	
	date = f"{year}.{month}.{day}"

	regions = d["values"]
	for region in regions:
		region_name = region["County"]
		if region_name in ["Illinois", "Cook", "Chicago"]:
			try:
				result[region_name][date]
			except:
				result[region_name][date] = {}

			result[region_name][date]["confirmed_cases"] = region["confirmed_cases"]
			result[region_name][date]["total_tested"] = region["total_tested"]
			result[region_name][date]["deaths"] = region["deaths"]

filename = f"{directory}\\formatted\\backfill.json"
if not os.path.exists(filename):
	json.dump(result, open(filename, "w"), indent="\t")
else:
	print("json file already exists")

filename = f"{directory}\\formatted\\dates.txt"
if not os.path.exists(filename):
	open(filename, "w").write("\n".join(dates))
else:
	print("dates file already exists")
