import datetime
import pytz
import json
import os

utc_now = datetime.datetime.utcnow()
tz = pytz.timezone('America/Chicago')
date = pytz.utc.localize(utc_now).astimezone(tz).date()
date_string = date.strftime("%Y.%m.%d")

directory = "C:\\Users\\Michael\\OneDrive - California Institute of Technology\\Documents\\musings, et cetera\\COVID-19\\IL data\\"

for line in open(f"{directory}\\formatted\\dates.txt", "r"):
	if date_string in line:
		print(f"today's data has already been formatted")
		exit(1)

result = {
	"Illinois": {},
	"Cook": {},
	"Chicago": {},
	"60630": {}
}

filename = f"{directory}COVIDTestResults_{date_string}.json"
if os.path.exists(filename):
	d = json.load(open(filename, "r"))
else:
	print("today's big-region data has not been downloaded yet; attempting to format yesterday's data...")
	date -= datetime.timedelta(days=1)
	date_string = date.strftime("%Y.%m.%d")

	filename = f"{directory}COVIDTestResults_{date_string}.json"
	if os.path.exists(filename):
		d = json.load(open(filename, "r"))
	else:
		print("yesterday's data does not exist; aborting")
		exit(1)

probables = d["probable_case_counts"]
result["Illinois"]["probable_cases"] = probables["probable_cases"]
result["Illinois"]["probable_deaths"] = probables["probable_deaths"]

regions = d["characteristics_by_county"]["values"]
for region in regions:
	region_name = region["County"]
	if region_name in ["Illinois", "Cook", "Chicago"]:
		result[region_name]["confirmed_cases"] = region["confirmed_cases"]
		result[region_name]["total_tested"] = region["total_tested"]
		result[region_name]["deaths"] = region["deaths"]

filename = f"{directory}COVIDZip_{date_string}.json"
if os.path.exists(filename):
	d = json.load(open(filename, "r"))
else:
	print(f"the zip code data for {date_string} has not been downloaded")
	exit(1)

zips = d["zip_values"]
for zip_code in zips:
	zip_code_number = zip_code["zip"]
	if zip_code_number == "60630":
		result["60630"]["confirmed_cases"] = zip_code["confirmed_cases"]
		result["60630"]["total_tested"] = zip_code["total_tested"]

json.dump(result, open(f"{directory}\\formatted\\today.json", "w"))

with open(f"{directory}\\formatted\\out.json", "r+") as fp:
	out = json.load(fp)
	for key in out.keys():
		try:
			out[key][date_string]
			print(f"today's data in {key} appears to already exist in out.json")
			exit(1)
		except:
			out[key][date_string] = result[key]
	fp.seek(0)
	fp.truncate()
	json.dump(out, fp, indent="\t")

open(f"{directory}\\formatted\\dates.txt", "a").write(f"{date_string}\n")

print("success")
