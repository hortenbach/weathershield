from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import Donnerwetter.Donnerwetter

logindatapath = "./data/login.meteo"

session = getMeteoSession(logindatapath)

# fetch example observation data
# the OAuth2Session will automatically handle adding authentication headers
params = {
    'locatedAt': '13,52',
    'observedPeriod': 'PT0S',
    'fields': 'airTemperatureInCelsius'
}
#data = session.get('https://point-observation.weather.mg/search', params=params)

data = session.get('https://point-forecast.weather.mg/search?fields=windSpeedInKilometerPerHour,clearSkyUVIndex&locatedAt=13.40675,52.51789&validPeriod=PT0S&validFrom=2018-01-11T14:00:00.000Z&validUntil=2018-01-26T14:00:00.000Z')

jsonResponse = json.loads(data.text)
jsonData = jsonResponse["forecasts"]
for forecast in jsonData:
    print(forecast.get("windSpeedInKilometerPerHour"))
    print(forecast.get("clearSkyUVIndex"))


#print ("RESPONSE DATA >>> " + data.text)
