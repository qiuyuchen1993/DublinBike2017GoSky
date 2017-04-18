import simplejson as json
from flask import Flask, g, jsonify
from sqlalchemy import create_engine
import MySQLdb

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
    return app.send_static_file('index.html')

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route('/user')
def root():
    return app.send_static_file('user.html')

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
    