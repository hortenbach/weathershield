#!/usr/bin/python3
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import json
import datetime
import Donnerwetter.Donnerwetter as d

now = datetime.datetime.now()
d.setBatteryChargingTime(3)

#write chronjob for charging within 5 days
d.setDeadline(now.year, now.month, now.day+5, now.hour)
d.shedule()
