from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import json
import datetime
import Donnerwetter.Donnerwetter as d

now = datetime.datetime.now()

logindatapath = "./data/login.meteo"

d.setBatteryChargingTime(3)
d.setDeadline(now.year, now.month, now.day+10, now.hour)

session = d.getMeteoSession(logindatapath)
wind = d.getWind(session)
print(wind)
solar = d.getSolar(session)
print(solar)
