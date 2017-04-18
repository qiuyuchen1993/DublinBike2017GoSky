import simplejson as json
from flask import Flask, g, jsonify
from sqlalchemy import create_engine
import MySQLdb
import config

config.connect_to_database()