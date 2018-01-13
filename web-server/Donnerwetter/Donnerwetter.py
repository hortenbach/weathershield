import json
import requests
import datetime
import Donnerwetter.sessionhandling as s
import Donnerwetter.Ladevorgang as lv

Ladevorgaenge = []

location = '13,52' #berlin

def addLadeVorgang(pin,year,month,day,hour,chargingTimeInHours):
    newLadevorgang = lv.Ladevorgang(pin,year,month,day,hour,chargingTimeInHours)
    newLadevorgang.newShedule()
    Ladevorgaenge.append(newLadevorgang)

def getAllLadevorgange():
    return Ladevorgaenge

def getLadevorgang(i):
    return Ladevorgaenge[i]

def removeLadevorgang(i):
    del Ladevorgaenge[i]

def serializeList():
    filename = 'DonnerwetterLadung.json'
    with open(filename, 'w') as f_obj:
        json.dump(Ladevorgaenge, f_obj)

def deserializeList():
    try:
        filename = 'DonnerwetterLadung.json'
        with open(filename) as f_obj:
            Ladevorgaenge = json.load(f_obj)
        print(numbers)
    except:
        Ladevorgaenge = []
