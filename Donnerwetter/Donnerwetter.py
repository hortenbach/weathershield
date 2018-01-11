from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import requests
import json
import requests
import numpy as np
import matplotlib.pyplot as plt
import datetime

location = '13,52' #berlin
token_url='https://auth.weather.mg/oauth/token'
forecastURL = 'https://point-forecast.weather.mg/search'
now = datetime.date.today()

params = {
    'locatedAt': location,
    'fields': 'windSpeedInKilometerPerHour,clearSkyUVIndex',
    'validPeriod': 'PT0S',
    'validFrom': ('{0}-{1:02d}-{2:02d}T14:00:00Z').format(now.year, now.month, now.day),
    'validUntil': ''
}

def setDeadline(doneUntil):
    params['validUntil'] = doneUntil

def getMeteoSession(logindatafile):
    """ Athenticate with logindata at Meteo API.
    Return Session.
    """
    with open(logindatafile, "r") as f:
        login = f.read().split()
        client_id = login[0]
        client_secret = login[1]
        f.close()

    client = BackendApplicationClient(client_id=client_id)
    client.prepare_request_body(scope=[])

    # fetch an access token
    session = OAuth2Session(client=client)
    session.fetch_token(token_url=token_url,
                        client_id=client_id,
                        client_secret=client_secret)
    return session

def getForecastData(session):
    data = session.get(forecastURL, params=params)
    return data

def getWind(session):
    data = getForecastData(session)
    jsonResponse = json.loads(data.text)
    jsonData = jsonResponse["forecasts"]
    wind = []
    for forecast in jsonData:
        wind.append(forecast.get("windSpeedInKilometerPerHour"))
    return wind

def getSolar(session):
    data = getForecastData(session)
    jsonResponse = json.loads(data.text)
    jsonData = jsonResponse["forecasts"]
    solar = []
    for forecast in jsonData:
        solar.append(forecast.get("clearSkyUVIndex"))
    return solar

def getOptimumChargingTime(winds, clouds, times, chargingTime):
    # Get Max
    winds_np = np.fromiter(winds, np.float)
    clouds_np = np.fromiter(clouds, np.float)

    windmax = winds_np.argmax() #Array position of max value
    print("[wind] max value ", winds_np[windmax], " on the ", times[windmax])
    print("[wind] values left of max ", winds_np[windmax-5:windmax])
    print("[wind] values righ of max ", winds_np[windmax+1:windmax+6])
    cloudmin = clouds_np.argmin() #Array position of max value
    print("[clouds]max value ", clouds_np[cloudmin], " on the ", times[cloudmin])
    print("[clouds] values left of max ", clouds_np[cloudmin+1:cloudmin+6,])

    windTimeSums = {}
    windTimeAVG = {}
    cloudTimeSums= {}
    cloudTimeAVG= {}

    for i in range(0, len(winds)-chargingTime):
        windTimeSums[times[i]] = np.sum(winds_np[i:i+chargingTime+1])
        windTimeAVG[times[i]] = np.average(winds_np[i:i+chargingTime+1])

    for i in range(0, len(clouds)-chargingTime):
        cloudTimeSums[times[i]] = np.sum(clouds_np[i:i+chargingTime+1])
        cloudTimeAVG[times[i]] = np.average(clouds_np[i:i+chargingTime+1])

    print("[wind] charging time with highest values starts on ")
    maximum_sums = max(windTimeSums, key=windTimeSums.get)  # Just use 'min' instead of 'max' for minimum.
    print(maximum_sums, windTimeSums[maximum_sums])
    print("[wind] charging time with highest average starts on ")
    maximum_avg = max(windTimeAVG, key=windTimeAVG.get)  # Just use 'min' instead of 'max' for minimum.
    print(maximum_avg, windTimeAVG[maximum_avg])

    print("[clouds] charging time with lowest values starts on ")
    minimum_sums = min(cloudTimeSums, key=cloudTimeSums.get)  # Just use 'min' instead of 'max' for minimum.
    print(minimum_sums, windTimeSums[minimum_sums])
    print("[clouds] charging time with lowest average starts on ")
    minimum_avg = min(cloudTimeAVG, key=cloudTimeAVG.get)  # Just use 'min' instead of 'max' for minimum.
    print(minimum_avg, cloudTimeAVG[minimum_avg])
    #TODO: find a shared Optimum between all Data
    # for now we use wind optimum as global optimum
    optimalTimeForCharging = maximum_avg
    return optimalTimeForCharging

def shedule(startTime):
    #now that we know a good time we write it to a file for chrone
    with open("./data/cronjobinfo", "w") as f:
            f.write(startTime) #TODO right format for crontab
            f.close()

def plotData(data):
    data_np = np.array(data)
    plt.plot(data_np, '-g')
    plt.plot()
    plt.show()

def plotDataAVG(winds, clouds, times):
    wind_np = np.fromiter(winds, np.float)
    clouds_np = np.fromiter(clouds, np.float)
    # Calculate the simple average of the data
    w_avg = [np.average(wind_np)]*len(wind_np)
    c_avg = [np.average(clouds_np)]*len(clouds_np)
    fig,ax = plt.subplots()
    # Plot the data
    data_line1 = ax.plot(wind_np, label='wind')
    data_line2 = ax.plot(clouds_np, label='clouds')
    # Plot the average line
    avg_line1 = ax.plot(w_avg, label='average', linestyle='--')
    avg_line1 = ax.plot(c_avg, label='average', linestyle='--')
    # Make a legend
    legend = ax.legend(loc='upper right')
    #plt.xticks(range(0,len(times), 50), times, rotation=45)
    plt.show()
