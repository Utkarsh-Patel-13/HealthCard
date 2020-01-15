import pymongo
from flask import Flask
#from flask_pymongo import PyMongo

app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Health"]
db = mydb["user"]


