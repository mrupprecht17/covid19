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
filename_list = os.listdir(directory)
for filename in filename_list:
	if "COVIDTestResults" in filename:
		date = filename.split("_")[1][:-5]
		dates.append(date) # assumes the date will also be in the ZIP code one
		d = json.load(open(directory + filename, "r"))

		try:
			result["Illinois"][date]
		except:
			result["Illinois"][date] = {}

		probables = d["probable_case_counts"]
		result["Illinois"][date]["probable_cases"] = probables["probable_cases"]
		result["Illinois"][date]["probable_deaths"] = probables["probable_deaths"]

		regions = d["characteristics_by_county"]["values"]
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

	elif "COVIDZip" in filename:
		date = filename.split("_")[1][:-5]
		d = json.load(open(directory + filename, "r"))

		try:
			result["60630"][date]
		except:
			result["60630"][date] = {}

		zips = d["zip_values"]
		for zip_code in zips:
			zip_code_number = zip_code["zip"]
			if zip_code_number == "60630":
				result["60630"][date]["confirmed_cases"] = zip_code["confirmed_cases"]
				result["60630"][date]["total_tested"] = zip_code["total_tested"]

if not os.path.exists(f"{directory}\\formatted\\out.json"):
	json.dump(result, open(f"{directory}\\formatted\\out.json", "w"), indent="\t")
else:
	print("json file already exists")

if not os.path.exists(f"{directory}\\formatted\\dates.txt"):
	open(f"{directory}\\formatted\\dates.txt", "w").write("\n".join(dates))
else:
	print("dates file already exists")
