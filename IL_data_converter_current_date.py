import json
import os

directory = "C:\\Users\\Michael\\OneDrive - California Institute of Technology\\Documents\\musings, et cetera\\COVID-19\\IL data\\formatted\\"

filename = f"{directory}today.json"
if os.path.exists(filename):
	d = json.load(open(filename, "r"))
else:
	print(f"{filename} doesn't exist")
	exit(1)

zp = d["60630"]["confirmed_cases"]
zt = d["60630"]["total_tested"]
open(f"{directory}60630.csv", "w").write(f",,,,,,,,{zt},,,,,,,,,,,,{zp}")

for c in ["Cook", "Chicago", "Illinois"]:
	cp = d[c]["confirmed_cases"]
	ct = d[c]["total_tested"]
	cd = d[c]["deaths"]

	if c == "Cook":
		cp += d["Chicago"]["confirmed_cases"]
		ct += d["Chicago"]["total_tested"]
		cd += d["Chicago"]["deaths"]

	out_string = f",,,,,,{cd},,{ct},,,,,,,,,,,,,,{cp}"

	if c == "Illinois":
		try:
			ilpp = d["Illinois"]["probable_cases"]
			ilpd = d["Illinois"]["probable_deaths"]
			out_string += f",{ilpp},{ilpd}"
		except KeyError:
			print("probable counts missing")
	
	open(f"{directory}{c}.csv", "w").write(out_string)

print("success")
