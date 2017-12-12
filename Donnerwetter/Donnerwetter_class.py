from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import requests
import json
import requests
import numpy as np
import matplotlib.pyplot as plt
import datetime


class Donnerwetter:
    def __init__(self, client_id, client_secret, params, chargingTime):
        ''' Constructor for this class. '''
        # Create some member animals
        self.members = ['winds', 'times', 'clouds']
        self.client = BackendApplicationClient(client_id=client_id)
        self.client.prepare_request_body(scope=[])
        self.params=params
        self.chargingTime = chargingTime
            
    def getDKForecast(self, doneInDays):
        #forecast area coordinates
        berlin = [52.520008, 13.404954]    
        data = {}
        now = datetime.date.today()
        winds = []
        clouds =[]
        times = []
        with open("./data/DarkSkyAPIkey.txt", "r") as f:
            key = f.readline()
        for i in range(0,doneInDays):
            r = requests.get(('https://api.darksky.net/forecast/{0}/{1},{2},{3}-{4}-{5:02d}T00:00:00Z?units=si').format(key,berlin[0],berlin[1],now.year,now.month,now.day+i))
            #DEBUG:
            #print(i, r.status_code)
            if r.status_code != 200:
                print ("Error fetching data from API . . . ",r.status_code)
            data=r.json()
        
            for d in data['hourly']['data']:
                times.append(datetime.datetime.fromtimestamp(d['time']).strftime("%A, %B %d, %Y %I:%M:%S"))
                winds.append(d['windSpeed'])
                clouds.append(d['cloudCover'])
                    
            # fetch an access token
            session = OAuth2Session(client=self.client)
            session.fetch_token(token_url='https://auth.weather.mg/oauth/token',
                                client_id=self.client_id,
                                client_secret=self.client_secret)
        return [winds, clouds, times]
        
    def getMeteorForecast(self):
        # fetch an access token
        session = OAuth2Session(client=self.client)
        session.fetch_token(token_url='https://auth.weather.mg/oauth/token',
                            client_id=self.client_id,
                            client_secret=self.client_secret)
        
        # access tokens are valid for one hour an can be re-used
        # print "ACCESS TOKEN (base64 encoded) >>> " + session.access_token
    
        #data = session.get('https://point-forecast.weather.mg/search?fields=averageWindSpeedInKilometerPerHour&locatedAt=13.40675,52.51789&validPeriod=PT24H,PT0S&validFrom=2017-12-12T14:00:00.000Z&validUntil=2017-12-27T14:00:00.000Z')
        data = session.get('https://point-observation.weather.mg/search', params=self.params)
        print ("RESPONSE DATA >>> " + data.text)
        return json.loads(data.text)
        
    def getOptimumChargingTime(self, winds, clouds, times):
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
        
        for i in range(0, len(winds)-self.chargingTime):
            windTimeSums[times[i]] = np.sum(winds_np[i:i+self.chargingTime+1])
            windTimeAVG[times[i]] = np.average(winds_np[i:i+self.chargingTime+1])
            
        for i in range(0, len(clouds)-self.chargingTime):
            cloudTimeSums[times[i]] = np.sum(clouds_np[i:i+self.chargingTime+1])
            cloudTimeAVG[times[i]] = np.average(clouds_np[i:i+self.chargingTime+1])
        
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


    def plotData(self,data):
        data_np = np.array(data)
        plt.plot(data_np, '-g')
        plt.plot()
        plt.show()
    
    def plotDataAVG(self, winds, clouds, times):
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
        