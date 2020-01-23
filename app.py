from pymongo import MongoClient
from flask import Flask

app = Flask(__name__)

client = MongoClient('localhost', 27017)
health_db = client.Health
db_user = health_db.user
db_doc = health_db.doctor


