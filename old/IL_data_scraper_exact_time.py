from urllib.request import urlopen, urlretrieve
import datetime
import pytz
import json

utc_now = datetime.datetime.utcnow()
tz = pytz.timezone('America/Chicago')
_date = pytz.utc.localize(utc_now).astimezone(tz)
dt = _date.strftime("%Y.%m.%d %H%M %Z")
# print(date)

filenames = [
	"COVIDHistoricalTestResults",
	"COVIDZip",
	"COVIDTestResults",
	"COVIDRates",
	"CountyDemos",
]

for filename in filenames:
	urlretrieve(f"http://www.dph.illinois.gov/sitefiles/{filename}.json?nocache=y",
		f"C:\\Users\\Michael\\OneDrive - California Institute of Technology\\Documents\\musings, et cetera\\COVID-19\\IL data\\{filename}_{dt}.json")
