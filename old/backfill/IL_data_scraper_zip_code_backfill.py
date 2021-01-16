from urllib.request import urlopen
import datetime
import json

directory = "C:\\Users\\Michael\\OneDrive - California Institute of Technology\\Documents\\musings, et cetera\\COVID-19\\IL data\\old zip code data\\"

date = datetime.date(year=2020, month=4, day=6)
today = datetime.date(year=2021, month=1, day=15)

while date < today:
	api_date_string = date.strftime("%Y-%m-%d")
	update_date_string = date.strftime("%Y.%m.%d")

	d = json.load(urlopen(f"https://idph.illinois.gov/DPHPublicInformation/api/COVID/GetZip?reportDate={api_date_string}"))
	json.dump(d, open(f"{directory}COVIDZip_{update_date_string}.json", "w"), indent="\t")

	date += datetime.timedelta(days=1)
