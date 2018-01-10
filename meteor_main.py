import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import Donnerwetter.Donnerwetter as dw


client_id = 'loginname'
client_secret = 'lalalala'  # SECRET! find a secure place to store, do NOT share

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
    'locatedAt': '13.40675,52.51789',
    'observedPeriod': 'PT24H',
    'fields': 'windSpeedInKilometerPerHour',
   # 'fields': 'lowCloudCoverInOcta',
    'validPeriod': 'PT24H,PT12H',
    'validFrom':'2018-01-07T23:00:00.000Z',
    'validUntil':'2018-01-22T23:00:00.000Z'
}

data = session.get('https://point-observation.weather.mg/search', params=params)

print ("RESPONSE DATA >>> " + data.text)
#client_id = 'p.waclaw'
#client_secret = '0Q85uXy9xn0VEQmZQeffp40SFZtWoonY'  # SECRET! find a secure place to store, do NOT share
#    
#client = BackendApplicationClient(client_id=client_id)
#client.prepare_request_body(scope=[])
#
## access tokens are valid for one hour an can be re-used
## print "ACCESS TOKEN (base64 encoded) >>> " + session.access_token
#
## fetch example observation data
## the OAuth2Session will automatically handle adding authentication headers
#params = {
#    #'locatedAt': '13,52',
#    'fields':'averageWindSpeedInKilometerPerHour',
#    'locatedAt':'13.40675,52.51789',
#    'validPeriod':'PT24H,PT0S',
#    'validFrom':'2017-12-12T14:00:00.000Z',
#    'validUntil':'2017-12-27T14:00:00.000Z'
#}
#
#
#requests.get('https://auth.weather.mg/oauth/token', auth=(client_id, client_secret))
## fetch an access token
##session = OAuth2Session(client=client)
##session.fetch_token(token_url='https://auth.weather.mg/oauth/token',
##                    client_id=client_id,
##                    client_secret=client_secret)
#
#data = requests.get('https://point-observation.weather.mg/search', params=params)
#
#print ("RESPONSE DATA >>> " + data.text)
#
#
##  
##
#chargingTime = 3 #in hours (data isnt more exact anyways)
##Our shedule:
##In how many days do we we want to be done (LESS OR EQUAL 14)
#doneInDays = 2
##what time do we want to be done?
#hourDone=8
#minuteDone=30

#data = dw.getMeteorForecast()
#startTime = dw.getOptimumChargingTime(data)
#
#dw.plotDataAVG(data)
#dw.shedule(startTime)
#
#
