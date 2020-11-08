from urllib.request import urlopen, urlretrieve
import datetime
import pytz
import json
import os

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

with urlopen("http://www.dph.illinois.gov/sitefiles/COVIDTestResults.json?nocache=y") as f:
	d = json.load(f)
	update_date_dict = d["LastUpdateDate"]
	update_date = datetime.datetime(**{component: update_date_dict[component] for component in ['year', 'month', 'day']}).date()
	update_date_string = update_date.strftime("%Y.%m.%d")
	mismatched_dates = date != update_date
	if mismatched_dates:
		for filename in filename_list:
			if update_date_string in filename:
				print("the data online has not been updated yet; try again later today (perhaps after 14:30 CT)")
				exit(1)

filenames = [
	"COVIDHistoricalTestResults",
	# "COVIDZip",
	"COVIDTestResults",
	"COVIDRates",
	"CountyDemos",
]

for filename in filenames:
	urlretrieve(f"http://www.dph.illinois.gov/sitefiles/{filename}.json?nocache=y",
		f"{directory}{filename}_{update_date_string}.json")
urlretrieve("https://idph.illinois.gov/DPHPublicInformation/api/COVID/GetZip",
	f"{directory}COVIDZip_{update_date_string}.json")
with open(f"{directory}COVIDZip_{update_date_string}.json", "r+") as fp:
	zips = json.load(fp)
	fp.seek(0)
	fp.truncate()
	json.dump(zips, fp, indent="\t")

if not mismatched_dates:
	print("success")
else:
	print("success (for yesterday's data)")
