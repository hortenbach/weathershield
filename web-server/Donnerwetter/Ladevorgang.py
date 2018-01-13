from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import json
import requests
from crontab import CronTab
import numpy as np
import matplotlib.pyplot as plt
import datetime
import Donnerwetter.sessionhandling as s

forecastURL = 'https://point-forecast.weather.mg/search'
logindatapath = './data/login.meteo'
now = datetime.datetime.now()
session = s.getMeteoSession(logindatapath)
batteryChargingTime = 0
location = '13,52' #berlin

params = {
    'locatedAt': location,
    'fields': 'windSpeedInKilometerPerHour,clearSkyUVIndex,cloudCoverLowerThan2000MeterInOcta,cloudCoverLowerThan5000MeterInOcta',
    'validPeriod': 'PT0S',
    'validFrom': ('{0}-{1:02d}-{2:02d}T{3:02d}:00:00Z').format(now.year, now.month, now.day, now.hour),
    'validUntil': ''
}


class Ladevorgang:
    def __init__(self,pin,year,month,day,hour,dauer):
        self.pin = pin
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.dauer = dauer
        self.starttime = None

    def getpin(self):
        return pin

    def getstarttime(self):
        return starttime

    def getdauer(self):
        return dauer

    def setDeadline(self,year, month, day, hour):
        if (hour-batteryChargingTime) < 0:
            day = day-1
            if day <= 0:
                month = month-1
                if month <= 0:
                    year = year-1
                    params['validUntil'] = ('{0}-{1:02d}-{2:02d}T{3:02d}:00:00Z').format(year, month, day, hour-batteryChargingTime)

    def setBatteryChargingTime(self,chargingTimeInHours):
        batteryChargingTime = chargingTimeInHours

    def setLoginDataPath(self,path):
        logindatapath = path

    def getMeteoSession(self,logindatapath):
        """ Athenticate with logindata at Meteo API.
        Return Session.
        """
        with open(logindatapath, "r") as f:
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

    def getForecastData(self,session=session):
        data = session.get(forecastURL, params=params)
        return data

    def getWind(self,session=session):
        data = getForecastData(session)
        jsonResponse = json.loads(data.text)
        jsonData = jsonResponse["forecasts"]
        wind = []
        for forecast in jsonData:
            wind.append(forecast.get("windSpeedInKilometerPerHour"))
        return wind

    def getCloudCoverage(self,session=session):
        data = getForecastData(session)
        jsonResponse = json.loads(data.text)
        jsonData = jsonResponse["forecasts"]
        cloud2000 = []
        cloud5000 = []
        timeline = []
        cloudtotal = []
        for forecast in jsonData:
            timeline.append(forecast.get("validUntil"))
            cloud2000.append(forecast.get("cloudCoverLowerThan2000MeterInOcta"))
            cloud5000.append(forecast.get("cloudCoverLowerThan5000MeterInOcta"))
        for i in range(len(timeline)):
            cloudtotal.append(cloud2000[i] + cloud5000[i])
        return cloudtotal

    def getUV(self,session=session):
        data = getForecastData(session)
        jsonResponse = json.loads(data.text)
        jsonData = jsonResponse["forecasts"]
        uv = []
        for forecast in jsonData:
            uv.append(forecast.get("clearSkyUVIndex"))
        return uv

    def getFTimes(self,session=session):
        data = getForecastData(session)
        jsonResponse = json.loads(data.text)
        jsonData = jsonResponse["forecasts"]
        times = []
        for forecast in jsonData:
            times.append(forecast.get("validUntil"))
        return times

    def printMax(self,source, times):
            source_np = np.fromiter(source, np.float)
            sourcemax = source_np.argmax() #Array position of max value
            print("max value ", source_np[sourcemax], " on the ", times[sourcemax])

    def peak(self,source, times):
        source_np = np.fromiter(source, np.float)
        sourceTimeSums = {}
        sourceTimeAVG = {}
        for i in range(0, len(source)-batteryChargingTime):
            sourceTimeSums[times[i]] = np.sum(source_np[i:i+batteryChargingTime+1])
            sourceTimeAVG[times[i]] = np.average(source_np[i:i+batteryChargingTime+1])
        maximum_sums = max(sourceTimeSums, key=sourceTimeSums.get)  # Just use 'min' instead of 'max' for minimum.
        return [maximum_sums,sourceTimeSums[maximum_sums]]

    def peakAVG(self,source, times):
        """ returns value and charging time with highest average """
        source_np = np.fromiter(source, np.float)
        sourceTimeSums = {}
        sourceTimeAVG = {}
        for i in range(0, len(source)-batteryChargingTime):
            sourceTimeSums[times[i]] = np.sum(source_np[i:i+batteryChargingTime+1])
            sourceTimeAVG[times[i]] = np.average(source_np[i:i+batteryChargingTime+1])
        maximum_avg = max(sourceTimeAVG, key=sourceTimeAVG.get)  # Just use 'min' instead of 'max' for minimum.
        return [maximum_avg, sourceTimeAVG[maximum_avg]]

    def peakMin(self,source, times):
        source_np = np.fromiter(source, np.float)
        sourceTimeSums = {}
        sourceTimeAVG = {}
        for i in range(0, len(source)-batteryChargingTime):
            sourceTimeSums[times[i]] = np.sum(source_np[i:i+batteryChargingTime+1])
            sourceTimeAVG[times[i]] = np.average(source_np[i:i+batteryChargingTime+1])
        minimum_sums = min(sourceTimeSums, key=sourceTimeSums.get)  # Just use 'min' instead of 'max' for minimum.
        return [minimum_sums,sourceTimeSums[minimum_sums]]

    def peakAVGmin(self, source, times):
        """ returns value and charging time with lowest average """
        source_np = np.fromiter(source, np.float)
        sourceTimeSums = {}
        sourceTimeAVG = {}
        for i in range(0, len(source)-batteryChargingTime):
            sourceTimeSums[times[i]] = np.sum(source_np[i:i+batteryChargingTime+1])
            sourceTimeAVG[times[i]] = np.average(source_np[i:i+batteryChargingTime+1])
        minimum_avg = min(sourceTimeAVG, key=sourceTimeAVG.get)  # Just use 'min' instead of 'max' for minimum.
        return [minimum_avg, sourceTimeAVG[minimum_avg]]

    def printOps(self):
        timedata = getFTimes()
        winddata = getWind()
        clouddata = getCloudCoverage()
        windOptimum = [peak(winddata, timedata), peakAVG(winddata, timedata)]
        cloudOptimum = [peakMin(clouddata, timedata), peakAVGmin(clouddata, timedata)]
        print("windoptimum >>>")
        print(windOptimum)
        print("cloud optimum >>>")
        print(cloudOptimum)

    def optimalTime(self):
        best = getOptimums()
        return best[1]

    def getOptimums(self):
        timedata = getFTimes()
        winddata = getWind()
        clouddata = getCloudCoverage()
        wind_np = np.fromiter(winddata, np.float)
        cloud_np = np.fromiter(clouddata, np.float)
        windSums = {}
        cloudSums = {}
        best = [0, 100]
        date = []
        # calculate the sum of all possible charging periods
        for i in range(len(timedata)-batteryChargingTime):
            windSums[timedata[i]] = np.sum(wind_np[i:i+batteryChargingTime+1])
            cloudSums[timedata[i]] = np.sum(cloud_np[i:i+batteryChargingTime+1])
            # windTimeAVG[timedata[i]] = np.average(wind_np[i:i+batteryChargingTime+1])
            # cloudTimeAVG[timedata[i]] = np.average(cloud_np[i:i+batteryChargingTime+1])
        # find day where winds are high and clouds are low
        for i in range(len(timedata)):
            if windSums[timedata[i]] >= best[0]:
                #print ("true")
                if cloudSums[timedata[i]] <= best[1]:
                    #print ("true2")
                    best = [windSums[timedata[i]], cloudSums[timedata[i]]]
                    date = timedata[i]
        return [best, date]

    def newShedule(self):
        if self.pin == '1':
            print("holla 1")
            cron=CronTab(user='pi')
            cronjob=cron.new(command='~/weathershield/bash/gpio19ON.sh')
            cronjob.setall(('0 {hour} {day} {month} *').format(hour=hour, day=day, month=month))       
            cron.write()
        if self.pin == '2':
            print("Holla 2")
            cron=CronTab(user='pi')
            cronjob=cron.new(command='~/weathershield/bash/gpio26ON.sh')
            cronjob.setall(('0 {hour} {day} {month} *').format(hour=hour, day=day, month=month))        
            cron.write()

    def plotData(self,data):
        data_np = np.array(data)
        plt.plot(data_np, '-g')
        plt.plot()
        plt.show()

    def plotDataAVG(self,source1, source2, times):
        source1_np = np.fromiter(source1, np.float)
        source2_np = np.fromiter(source2, np.float)
        # Calculate the simple average of the data
        w_avg = [np.average(source1_np)]*len(source1_np)
        c_avg = [np.average(source2_np)]*len(source2_np)
        fig,ax = plt.subplots()
        # Plot the data
        data_line1 = ax.plot(source1_np, label='wind')
        data_line2 = ax.plot(source2_np, label='source2')
        # Plot the average line
        avg_line1 = ax.plot(w_avg, label='average', linestyle='--')
        avg_line1 = ax.plot(c_avg, label='average', linestyle='--')
        # Make a legend
        legend = ax.legend(loc='upper right')
        #plt.xticks(range(0,len(times), 50), times, rotation=45)
        plt.show()
