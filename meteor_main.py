#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
NOTES:

"""
from oauthlib.oauth2 import BackendApplicationClient
#from requests_oauthlib import OAuth2Session
import Donnerwetter as dw

client_id = 'login.name'
client_secret = 'yxyxyxyxyxy'  # SECRET! find a secure place to store, do NOT share

client = BackendApplicationClient(client_id=client_id)
client.prepare_request_body(scope=[])
  

chargingTime = 3 #in hours (data isnt more exact anyways)
#Our shedule:
#In how many days do we we want to be done (LESS OR EQUAL 14)
doneInDays = 2
#what time do we want to be done?
hourDone=8
minuteDone=30

params = {
    #'locatedAt': '13,52',
    'fields':'averageWindSpeedInKilometerPerHour',
    'locatedAt':'13.40675,52.51789',
    'validPeriod':'PT24H,PT0S',
    'validFrom':'2017-12-12T14:00:00.000Z',
    'validUntil':'2017-12-27T14:00:00.000Z'
}

data = dw.getDKForecast(doneInDays, doneInDays, client, client_id, client_secret)
startTime = dw.getOptimumChargingTime(data)


dw.plotDataAVG(data)
dw.shedule(startTime)
