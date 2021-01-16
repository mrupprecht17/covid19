import datetime
import json
import os

directory = "C:\\Users\\Michael\\OneDrive - California Institute of Technology\\Documents\\musings, et cetera\\COVID-19\\IL data\\formatted\\"

filename = f"{directory}backfill.json"
if os.path.exists(filename):
	_d = json.load(open(filename, "r"))
else:
	print(f"{filename} doesn't exist")
	exit(1)

out_strings = {
	"Illinois": [],
	"Cook": [],
	"Chicago": [],
	"60630": []
}

iter_date = datetime.datetime(2020, 3, 17).date()
end_date = datetime.datetime(2020, 7, 4).date()
while iter_date <= end_date:
	no_60630 = False

	iter_date_string = iter_date.strftime("%Y.%m.%d")
	iter_date += datetime.timedelta(days=1)

	if iter_date_string == "2020.03.23":
		for c in ["Chicago", "Cook", "Illinois"]:
			out_strings[c].append(",,,,,,,,,,,,,,,,,,,,,,")
		continue

	d = {}
	for key in _d.keys():
		try:
			d[key] = _d[key][iter_date_string]
		except KeyError:
			print(f"{iter_date_string} has no data for {key}")
			if key == "60630":
				no_60630 = True
			else:
				exit(1)
	
	if not no_60630:
		zp = d["60630"]["confirmed_cases"]
		zt = d["60630"]["total_tested"]
		out_strings["60630"].append(f",,,,,,,,{zt},,,,,,,,,,,{zp}")
	else:
		out_strings["60630"].append("")

	for c in ["Chicago", "Cook", "Illinois"]:
		cp = d[c]["confirmed_cases"]
		ct = d[c]["total_tested"]
		cd = d[c]["deaths"]

		if c == "Cook":
			cp += d["Chicago"]["confirmed_cases"]
			ct += d["Chicago"]["total_tested"]
			cd += d["Chicago"]["deaths"]

		out_string = f",,,,,,{cd},,{ct},,,,,,,,,,,,,,{cp}"
		
		out_strings[c].append(out_string)

for key in out_strings.keys():
	filename = f"{directory}{key}.csv"
	if not os.path.exists(filename):
		open(filename, "w").write("\n".join(out_strings[key]))
	else:
		print(f"{filename} already exists")
