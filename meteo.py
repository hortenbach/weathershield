from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import json
import datetime
import Donnerwetter.Donnerwetter as d

now = datetime.datetime.now()

d.setBatteryChargingTime(3)
d.setDeadline(now.year, now.month, now.day+10, now.hour)

wind = d.getWind()
print(wind)
solar = d.getUV()
print(solar)
times = d.getFTimes()
print('highest single value:', d.peak(wind, times))
print('start of best charging period:', d.peakAVG(wind, times))
