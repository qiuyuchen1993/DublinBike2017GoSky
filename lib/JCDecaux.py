'''
Created on Mar 27, 2017
@author: dell-pc
'''
import requests
import traceback
import datetime
import time
import json

from sqlalchemy import create_engine




APIKEY = '39662f912f908f18cf2e03b0dfaa00123d488637'
STATIONS = 'https://api.jcdecaux.com/vls/v1/stations'
NAME="Dublin"
json1=0
# comment
URI="bikesdb.cvaowyzhojfp.eu-west-1.rds.amazonaws.com"
PORT = "3306"
DB = "dbikes"
USER = "teamgosky"
PASSWORD = "teamgosky"
engine = create_engine("mysql+mysqldb://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)
sql = """
CREATE DATABASE IF NOT EXISTS dbikes;
"""
engine.execute(sql)
sql = """
CREATE TABLE IF NOT EXISTS station (
Number INTEGER,
Name VARCHAR(256),
Address VARCHAR(256),
Position_lat REAL,
Position_lng REAL,
Banking BIT,
Bonus BIT,
Status VARCHAR(256),
Contract_name VARCHAR(256),
Bike_stands INTEGER,
Available_bike_stands INTEGER,
Available_bikes INTEGER, 
Last_update VARCHAR(256)
)
"""
try:
    res = engine.execute("DROP TABLE IF EXISTS station")
    res = engine.execute(sql)
    print(res.fetchall())
except Exception as e:
    print(e)

def write_to_file(r):
    with open("app.json".format(datetime.datetime.now()).replace(" ","_"), "w") as f:
        f.write(json.dumps(r))
 

def main():
    while True:
        try:
            #now = datetime.now()
            r = requests.get(STATIONS, params={"apiKey":APIKEY, "contract":NAME})
            global json1 
            json1=json.loads(r.text)
            print(len(json1))
            write_to_file(json1)
            write_to_db(r)
            time.sleep(5*60)
        except:
            print(traceback.format_exc())
            #if engine is None:
    return

def write_to_db(text):
    stations = json1
    print(type(stations), len(stations))
    print(stations)
    for station in stations:
        print(station)
        vals = (station.get('number'),station.get('name'),station.get('address'),station.get('position').get('lat'), station.get('position').get('lng'), 
                int(station.get('banking')), int(station.get('bonus')),station.get('status'), 
                station.get('contract_name'),station.get('bike_stands'),station.get('available_bike_stands'),
                station.get('available_bikes'),station.get('last_update'))
        engine.execute("insert into station values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", vals)
    return
    

main()