from urllib.request import urlopen
import json
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import datetime
import sys

metro_pops1 = {
	"Chicago": 9.5e6,
	"San Jose": 2.0e6
}
metro_pops2 = {
	"Atlanta": 6.0e6,
	# "Kansas City": 2.1e6,
	"New Orleans": 1.3e6,
	"Miami": 6.2e6,
	"Houston": 7.0e6,
	# "Minneapolis": 3.3e6,
	# "Charlotte": 2.6e6,
	"New York": 20.3e6,
	"Los Angeles": 13.1e6,
	"San Francisco": 4.7e6,
	"Boston": 4.6e6,
	"Phoenix": 4.9e6
}

start_date = "2020-03-01"
start = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
last = datetime.datetime.today().date()
days_since_start = (datetime.datetime.today().date() - start).days

metro_pops = dict(metro_pops2, **metro_pops1)
metro_pops = metro_pops1

hashes = [
	"2e2bff255977a3d1e7ca7d5046f7f9d726414613",
	"3ae02e65625d02292ec0be98d8044fe38bb58be4",
	"1edc90f6c2c7ab866ebecd97bcfaa01086ff3557",
	"9f1050a80da460a224a183a60ccf8cbf8d5d4d51",
	"47e1ec01d4843d366bceae29f597e6a7b6859873",
	"a6283dc2280307e8bf92a302800dd2dd523aa758",
	"7bb5d51282cbb6e79d5d29edc22c97d97cffcbc3",
	"57ac16bc5c2cc39faff4a67474bbcc627af30ed4",
	"615443c83578120dfdbc0c56ca10172f6e30124e"
]

with urlopen(f"https://static01.nyt.com/newsgraphics/2020/03/16/coronavirus-maps/{hashes[-1]}/data/metros/timeseries.json") as f:
	a = json.load(f)

cities = metro_pops.keys()

fig, ax = plt.subplots()
for d in a["data"]:
	for city in cities:
		# all_cases_plot = plt.figure(1)
		# cases_per_capita_plot = plt.figure(2)
		if city in d["display_name"] and "-" in d["display_name"]:
			# print(d["first"], city)
			first = datetime.datetime.strptime(d["first"], "%Y-%m-%d").date()
			# last = datetime.datetime.strptime(d["last"], "%Y-%m-%d").date()
			# print(first)
			diff = (first - start).days
			# print(diff)
			all_cases = np.array(([0] * diff) + d["all_cases"])[:-1]
			# print(all_cases[:-1])
			# print(all_cases[1:])
			cases_per_capita = all_cases / metro_pops[city]

			# days_since_start = (last - start).days + 1
			dates = [start + datetime.timedelta(days=offset) for offset in range(days_since_start - 1)]

			# plt.figure(1)
			# plt.plot(all_cases[1:] - all_cases[:-1])

			# plt.figure(2)
			# print(first, last, city)
			ax.plot(dates, cases_per_capita[1:] - cases_per_capita[:-1], label=city)
plt.legend()
# fig, _ = plt.subplots()
# print(plt.subplots())
fig.autofmt_xdate()
plt.show()
