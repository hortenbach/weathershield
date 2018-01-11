from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import json

import Donnerwetter.Donnerwetter as d

logindatapath = "./data/login.meteo"

session = d.getMeteoSession(logindatapath)
d.setDeadline('2018-01-26T14:00:00.000Z')
wind = d.getWind(session)
print(wind)
solar = d.getSolar(session)
print(solar)
