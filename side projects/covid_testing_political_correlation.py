from urllib.request import urlopen
import json
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import statsmodels.api as sm

state_data = {}

directory = "C:\\Users\\Michael\\OneDrive - California Institute of Technology\\Documents\\musings, et cetera\\COVID-19\\"
with open(f"{directory}states.tsv", "r") as fp:
	for line in fp:
		try:
			state, governor, house, senate = line.split("\t")
		except ValueError:
			state, governor, house, senate, _ = line.split("\t")

		state_data[state] = {
			"governor": governor
		}

		for chamber_string in ["house", "senate"]:
			# I'm counting Nebraska's senate as its house
			if not state == "Nebraska":
				chamber = eval(chamber_string)
			else:
				chamber = senate

			chamber = chamber.split(" ")
			chamber[1] = chamber[1].split("-")

			i = 0
			while i < len(chamber[1]):
				chamber[1][i] = int(chamber[1][i])
				i += 1

			while len(chamber[1]) < 4:
				chamber[1].append(0)

			# majority over all occupied seats (that is, not counting vacancies)
			majority_percent = chamber[1][0] / (chamber[1][0] + chamber[1][1] + chamber[1][3])
			veto_proof = majority_percent >= 2/3

			if chamber[0] == "R":
				chamber[1][0], chamber[1][1] = chamber[1][1], chamber[1][0]

			democratic_two_party_share = chamber[1][0] / (chamber[1][0] + chamber[1][1])

			state_data[state][chamber_string] = {
				"control": chamber[0],
				"veto_proof": veto_proof,
				"majority_percent": majority_percent,
				"democratic_two_party_share": democratic_two_party_share,
				"dem": chamber[1][0],
				"rep": chamber[1][1],
				"vac": chamber[1][2],
				"ind": chamber[1][3]
			}

		if state_data[state]["house"]["control"] == state_data[state]["senate"]["control"]:
			state_data[state]["legislature_control"] = state_data[state]["house"]["control"]
			state_data[state]["double_veto_proof"] = state_data[state]["house"]["veto_proof"] and state_data[state]["senate"]["veto_proof"]
			state_data[state]["trifecta"] = state_data[state]["legislature_control"] == state_data[state]["governor"]
		else:
			state_data[state]["legislature_control"] = "split"
			state_data[state]["double_veto_proof"] = False
			state_data[state]["trifecta"] = False

hashes = [
	"2ba0c6a9800c51b75515a4aa4c8515ff9f5e5375"
]

a = json.load(urlopen(f"https://static01.nyt.com/newsgraphics/2020/06/02/testing-dashboard/{hashes[-1]}/states_recent.json"))

for d in a:
	state = d["name"]
	try:
		state_data[state]["test_pct"] = d["latest_d"]["test_pct"]
	except KeyError: # we only want the states already in the list (all of them)
		pass

governors = []
houses = []
senates = []
legislatures = []
double_veto_proofs = []
trifectas = []
test_pcts = []

for state in state_data:
	s = state_data[state]

	if s["governor"] == "D":
		governors.append(1)
	else:
		governors.append(0)

	houses.append(s["house"]["democratic_two_party_share"])
	senates.append(s["senate"]["democratic_two_party_share"])

	if s["legislature_control"] == "D":
		legislatures.append(1)

		if s["double_veto_proof"]:
			double_veto_proofs.append(1)
		else:
			double_veto_proofs.append(0)

		if s["governor"] == "D":
			trifectas.append(1)
		else:
			trifectas.append(0)
	elif s["legislature_control"] == "split":
		legislatures.append(0)
		double_veto_proofs.append(0)
		trifectas.append(0)
	else:
		legislatures.append(-1)

		if s["double_veto_proof"]:
			double_veto_proofs.append(-1)
		else:
			double_veto_proofs.append(0)

		if s["governor"] == "R":
			trifectas.append(-1)
		else:
			trifectas.append(0)

	test_pcts.append(s["test_pct"])

governors = np.array(governors)
houses = np.array(houses)
senates = np.array(senates)
legislatures = np.array(legislatures)
double_veto_proofs = np.array(double_veto_proofs)
trifectas = np.array(trifectas)
test_pcts = np.array(test_pcts)

# X = np.column_stack((governors, houses, senates, legislatures, double_veto_proofs, trifectas))
# X = np.column_stack((governors, legislatures, double_veto_proofs, trifectas))
# X = houses
X = trifectas
X = sm.add_constant(X)
y = test_pcts

model = sm.OLS(y, X)
results = model.fit()
print(results.summary())

# fig, ax = plt.subplots()
for predictor in [governors, houses, senates, legislatures, double_veto_proofs, trifectas]:
	# print(predictor, test_pcts)
	plt.scatter(predictor, test_pcts)
	# plt.show()
# plt.legend()
# fig, _ = plt.subplots()
# print(plt.subplots())
# fig.autofmt_xdate()
# plt.show()
