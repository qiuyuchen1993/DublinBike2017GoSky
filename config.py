import simplejson as json
from flask import Flask, g, jsonify, render_template
from sqlalchemy import create_engine
import MySQLdb
import pandas as pd

#static_url_path=''
app = Flask(__name__)

URI="bikesdb.cvaowyzhojfp.eu-west-1.rds.amazonaws.com"
PORT = "3306"
DB = "dbikes"
USER = "teamgosky"
PASSWORD = "teamgosky"

def connect_to_database():
    db_str = "mysql+mysqldb://{}:{}@{}:{}/{}"
    engine = create_engine(db_str.format(USER, PASSWORD, URI, PORT, DB), echo=True)
    return engine
#    db = MySQLdb.connect(host="localhost",user="teamgosky",passwd="teamgosky",db="dbikes")
#    return db

def get_db():
    engine = getattr(g, 'engine', None)
    if engine is None:
        engine = g.engine = connect_to_database()
    return engine

@app.route("/all")
#@functools.lru_cache(maxsize=128)
def get_station():
    engine=get_db()
    sql="select * from station;"
    rows = engine.execute(sql).fetchall()
    print('#found{}stations',len(rows))
    return jsonify(stations=[dict(row.items()) for row in rows])
    

@app.route("/available/<int:Number>")
def get_stations(Number):
    engine=get_db()
#    cc = connect_to_database()
#    cur = cc.cursor()
    data = []
    rows = engine.execute("SELECT available_bikes from station where Number = {};".format(Number))
    for row in rows:
        data.append(dict(row))    
    return json.dumps(data)

@app.route("/")
def main():
    return "Hi!"

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route('/user')
def root():
    return render_template('user.html')

@app.route('/station/<int:Number>')
def station(Number):
    print(Number)
    sql="""
    select * from station where number = {}
    """.format(Number)
    engine = get_db()
    rows = engine.execute(sql).fetchall()
    res = [dict(row.items()) for row in rows]
    return jsonify(data=res)

@app.route("/dbinfo")
def get_dbinfo():
    sql="""
    SELECT table_name FROM information_schema.tables
    where table_schema='{}';
    """.format(DB)
    engine = get_db()
    rows = engine.execute(sql).fetchall()
    res = [dict(row.items()) for row in rows]
    print(res)
    return jsonify(data=res)

@app.route("/occupancy/<int:Number>")
def get_occupany(Number):
    engine=get_db()
    df = pd.read_sql_query("select * from availability where Number = %(Number)s", engine, params={"Number":Number})
    df['Last_update']=pd.to_datetime(df.Last_update, unit='ms')
    df.set_index('Last_update', inplace=True)
    res = df['Available_bike_stands'].resample('5m').mean()
    print(res)
    return jsonify(data=json.dumps(list(zip(map(lambda x:x.isoformat(), res.index), res.values))))

if __name__=="__main__":
    """
    The URLs you should visit after starting the app:
    http://127.0.0.1:5000/
    http://127.0.0.1:5000/hello
    http://127.0.0.1:5000/user
    http://127.0.0.1:5000/dbinfo
    http://127.0.0.1:5000/station/42
    """
    app.run(debug=True)
    