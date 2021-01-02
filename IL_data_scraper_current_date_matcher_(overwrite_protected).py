from urllib.request import urlopen, urlretrieve
import urllib
import datetime
import pytz
import json
import os

def keep_retrying(zip_values, i):
	try:
		zip_values[i]["demographics"] = json.load(urlopen(
			f"https://idph.illinois.gov/DPHPublicInformation/api/COVID/GetZipDemographics?zipCode={zip_values[i]['zip']}"))
	except (urllib.error.URLError, ConnectionResetError):
		keep_retrying(zip_values, i)

utc_now = datetime.datetime.utcnow()
tz = pytz.timezone('America/Chicago')
date = pytz.utc.localize(utc_now).astimezone(tz).date()
date_string = date.strftime("%Y.%m.%d")
# print(date)

directory = "C:\\Users\\Michael\\OneDrive - California Institute of Technology\\Documents\\musings, et cetera\\COVID-19\\IL data\\"
filename_list = os.listdir(directory)
for filename in filename_list:
	if date_string in filename:
		s = input("today's data has already been recorded; re-record (y/n)? ")
		if s != "y":
			exit(1)
		else:
			break

with urlopen("https://idph.illinois.gov/DPHPublicInformation/api/COVID/GetCountyTestResults") as f:
	d = json.load(f)
	update_date_dict = d["lastUpdatedDate"]
	update_date = datetime.datetime(**{component: update_date_dict[component] for component in ['year', 'month', 'day']}).date()
	update_date_string = update_date.strftime("%Y.%m.%d")
	mismatched_dates = date != update_date
	if mismatched_dates:
		for filename in filename_list:
			if update_date_string in filename:
				print("the data online has not been updated yet; try again later today (perhaps after 14:30 CT)")
				exit(1)

api_names = {
	# "COVIDHistoricalTestResults": f"GetCountyHistoricalTestResults?reportDate={update_date_string}",
	# "COVIDZip": "GetZip",
	"COVIDTestResults": "GetCountyTestResults",
	"COVIDRates": "GetCountyRates",
	"CountyDemos": "GetCountyDemographics",
}

for old_name in api_names:
	json.dump(json.load(urlopen(f"https://idph.illinois.gov/DPHPublicInformation/api/COVID/{api_names[old_name]}")),
		open(f"{directory}{old_name}_{update_date_string}.json", "w"), indent="\t")

d = json.load(urlopen("https://idph.illinois.gov/DPHPublicInformation/api/COVID/GetZip"))
zip_values = d["zip_values"]
i = 0
while i < len(zip_values):
	keep_retrying(zip_values, i)
	i += 1
json.dump(d, open(f"{directory}COVIDZip_{update_date_string}.json", "w"), indent="\t")

if not mismatched_dates:
	print("success")
else:
	print("success (for yesterday's data)")
