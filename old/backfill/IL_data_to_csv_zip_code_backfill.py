import datetime
import json
import os
import pandas as pd

result = []

date = datetime.date(year=2020, month=4, day=6)
today = datetime.date(year=2021, month=1, day=15)

directory = "C:\\Users\\Michael\\OneDrive - California Institute of Technology\\Documents\\musings, et cetera\\COVID-19\\IL data\\old zip code data\\"
while date < today:
	update_date_string = date.strftime("%Y.%m.%d")

	full_filename = f"{directory}COVIDZip_{update_date_string}.json"
	if os.path.exists(full_filename):
		d = json.load(open(full_filename, "r"))
	else:
		print(f"the zip code data for {update_date_string} has not been downloaded")
		exit(1)

	zips = d["zip_values"]
	for zip_code in zips:
		zip_code_number = zip_code["zip"]
		if zip_code_number == "60630":
			result.append((str(date), zip_code["confirmed_cases"], zip_code["total_tested"]))

	date += datetime.timedelta(days=1)

df = pd.DataFrame(result, columns=["date", "confirmed_cases", "total_tested"])
df.to_csv(f"{directory}formatted\\60630.csv")
