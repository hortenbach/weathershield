#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
NOTES:
    In order to access data we have to create a folder named "data" in 
    the same directory as this file and create a file "DarkSkyAPIkey.txt"
    there, which holds an valid access key in the first line. 
    
    newScan = 1 does a complete request at the API and fecthes data.
    newScan = 0 for programming and debugging because we don't want to reload/
	     request again each time we change the code. 
"""
#https://api.darksky.net/forecast/[key]/[latitude],[longitude]
newScan = 1
chargingTime = 3 #in hours (data isnt more exact anyways)

#Our shedule:
#In how many days do we we want to be done (LESS OR EQUAL 14)
doneInDays = 7
#what time do we want to be done?
hourDone=8
minuteDone=30

if newScan: 
    import requests
    import numpy as np
    import matplotlib.pyplot as plt
    import datetime
    import Donnerwetter.Donnerwetter as dw
    #forecast area coordinates
    berlin = [52.520008, 13.404954]    
    data = {}
    now = datetime.date.today()

    winds = []
    times = []
    clouds =[]
    with open("./data/DarkSkyAPIkey.txt", "r") as f:
        key = f.readline()
    for i in range(0,doneInDays):
        r = requests.get(('https://api.darksky.net/forecast/{0}/{1},{2},{3}-{4:02d}-{5:02d}T00:00:00Z?units=si').format(key,berlin[0],berlin[1],now.year,now.month,now.day+i))
        #DEBUG:
        #print(i, r.status_code)
        if r.status_code != 200:
            print ("Error fetching data from API . . . ",r.status_code)
        data=r.json()

        for d in data['hourly']['data']:
            times.append(datetime.datetime.fromtimestamp(d['time']).strftime("%A, %B %d, %Y %I:%M:%S"))
            winds.append(d['windSpeed'])
            clouds.append(d['cloudCover'])
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
minimum_sums = min(windTimeSums, key=windTimeSums.get)  # Just use 'min' instead of 'max' for minimum.
print(maximum_sums, windTimeSums[maximum_sums])
print("[clouds] charging time with lowest average starts on ")
minimum_avg = min(windTimeAVG, key=windTimeAVG.get)  # Just use 'min' instead of 'max' for minimum.
print(maximum_avg, windTimeAVG[maximum_avg])

dw.plotDataAVG(winds_np, clouds_np, times)

chargingTime = 0
'''
TODO algorithm to choose how to shedule
if maxWind ==maxSun:
    chargingTime = max....
else
    ......
'''
chargingTime = maximum_avg

#now that we know a good time we write it to a file for chrone
with open("./data/cronjobinfo", "w") as f:
        f.write(chargingTime) #TODO right format for crontab
        f.close()
