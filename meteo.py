from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import json

with open("./data/login.meteo", "r") as f:
        login = f.read().split()
        client_id = login[0]
        client_secret = login[1]
        f.close()

client = BackendApplicationClient(client_id=client_id)
client.prepare_request_body(scope=[])

# fetch an access token
session = OAuth2Session(client=client)
session.fetch_token(token_url='https://auth.weather.mg/oauth/token',
                    client_id=client_id,
                    client_secret=client_secret)

# access tokens are valid for one hour an can be re-used
# print "ACCESS TOKEN (base64 encoded) >>> " + session.access_token

# fetch example observation data
# the OAuth2Session will automatically handle adding authentication headers
params = {
    'fields': 'windSpeedInKilometerPerHour,clearSkyUVIndex',
    'locatedAt': '13.40675,52.51789',
    'validPeriod': 'PT0S',
    'validFrom':'2018-01-11T14:00:00.000Z',
    'validUntil':'2018-01-26T14:00:00.000Z'
}
data = session.get('https://point-forecast.weather.mg/search', params=params)

jsonResponse = json.loads(data.text)
jsonData = jsonResponse["forecasts"]
for forecast in jsonData:
    print(forecast.get("windSpeedInKilometerPerHour"))
    print(forecast.get("clearSkyUVIndex"))


#print ("RESPONSE DATA >>> " + data.text)
