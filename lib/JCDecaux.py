import requests
import traceback
import datetime
import time
import json
import sqlite3

APIKEY = '39662f912f908f18cf2e03b0dfaa00123d488637'
STATIONS = 'https://api.jcdecaux.com/vls/v1/stations'
NAME="Dublin"

# comment

def write_to_file(r):
    with open("test.json".format(datetime.datetime.now()).replace(" ","_"), "w") as f:
        f.write(json.dumps(r))
 
def write_to_db(text):
    pass 
    
def main():
    while True:
        try:
            #now = datetime.now()
            r = requests.get(STATIONS, params={"apiKey":APIKEY, "contract":NAME})
            json1 =json.loads(r.text)
            write_to_file(json1)
            write_to_db(r)
            time.sleep(5*60)
        except:
            print(traceback.format_exc())
            #if engine is None:
    return

main()