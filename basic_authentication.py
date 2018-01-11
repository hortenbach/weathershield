from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import json
import Donnerwetter.Donnerwetter as d

logindatapath = "./data/login.meteo"

session = d.getMeteoSession(logindatapath)

# fetch example observation data
# the OAuth2Session will automatically handle adding authentication headers
params = {
    'locatedAt': '13,52',
    'fields': 'windSpeedInKilometerPerHour,clearSkyUVIndex',
    'validPeriod': 'PT0S',
    'validFrom': '2018-01-14T14:00:00.000Z',
    'validUntil': '2018-01-16T14:00:00.000Z'
}
data = session.get('https://point-forecast.weather.mg/search', params=params)

jsonResponse = json.loads(data.text)
jsonData = jsonResponse["forecasts"]
wind = []
solar = []
for forecast in jsonData:
    wind.append(forecast.get("windSpeedInKilometerPerHour"))
    solar.append(forecast.get("clearSkyUVIndex"))

print ("RESPONSE DATA >>> " + data.text)
print("wind and solar >>> ")
print(wind, solar)
