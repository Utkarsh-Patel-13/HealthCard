from pymongo import MongoClient
from flask import Flask

app = Flask(__name__)

client = MongoClient('localhost', 27017)
mydb = client.Health
db = mydb.user


