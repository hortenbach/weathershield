import json
import Donnerwetter.Donnerwetter as d
import Donnerwetter.Ladevorgang
import datetime
from enum import Enum
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

'''
class LoadType(Enum):
     AlwaysOn = 1
     OverLoad = 2
     Normal = 3

class Socket():
    """Represent a Socket."""
    def __init__(self, pin):
        self.pin = pin

class StorageSocket(Socket):
    def __init__(self, pin, LoadType, loadtime):
        super().__init__(pin)
        self.LoadType=LoadType
        self.loadtime=loadtime

class NormalSocket(Socket):
    def __init__(self, pin, LoadType):
        super().__init__(pin)
        self.LoadType = LoadType'''

# alles was vorher passieren muss
first_use = True
#versuche iene alte config wiederherzustellen
try:
    with open('conf/config.json') as json_file:
        settings = json.load(json_file)
        app.logger.debug('Found Configfile')
        first_use = False;
except:
    app.logger.debug('Can not load a config file - First use is assumed')

    '''battery = StorageSocket(12,2,1);
    normalSocket = NormalSocket(13,3);

    data = {
        'user':'admin'
        'adminpassword': '',
        'apiuser':'',
        'apikey':'',
        'geolatitude':'',
        'geolongitude':'',
        'wlanssid':'',
        'wlankey':'',
        'SocketCount':'2',
        'Sockets': [battery, normalSocket],
        }
    }'''

@app.route("/")
def main():
    '''if first_use:
        return redirect("/firstuse", code=302)
    else:'''
    Ladevorgaenge = d.getAllLadevorgange()
    templateData = {
       'Ladevorgaenge' : Ladevorgaenge
        }
    return render_template('main.html', **templateData )
    
@app.route("/firstuse", methods=['GET', 'POST'])
def firstuse():
    if request.method == 'POST':
        data = request.form
        first_use = false
        return render_template('completed.html')
    else:
        return render_template('firstuse.html')

@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        form = request.form
        pin = form.get('pinselect')
        deadlineTime = form.get('deadlineDateTime')
        deadlineTime = deadlineTime.split(':')
        deadline = form.get('deadlineDate')
        deadline = deadline.split('-')
        power = form.get('AH')
        print (pin)
        #TODO 24 hours time
        print (deadline)
        print (deadlineTime)
        print (power)
        d.addLadeVorgang(pin,deadline[0],deadline[1],deadline[2],deadlineTime[0],power)
        return render_template('completed.html')
    else:
        return render_template('add.html')


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
