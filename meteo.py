from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import json

import Donnerwetter.Donnerwetter as d

logindatapath = "./data/login.meteo"

session = d.getMeteoSession(logindatapath)

wind = d.getWind(session)
print(wind)
