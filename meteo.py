#!/usr/bin/python3
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import json
import datetime
import Donnerwetter.Donnerwetter as d

now = datetime.datetime.now()
d.setBatteryChargingTime(3)

#we want to charge within 5 days
d.setDeadline(now.year, now.month, now.day+5, now.hour)
#get optimal/greenest time to charge battery
bestTime = d.optimalTime()
print(bestTime)
d.printOps()
#set job for system to charge battery on optimal time
d.shedule()
