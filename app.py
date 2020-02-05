from pymongo import MongoClient
from flask import Flask
import dns

app = Flask(__name__)

client = MongoClient("mongodb+srv://SPUM:srinking69@myhealthcard-1nsmr.mongodb.net/test?retryWrites=true&w=majority")
health_db = client.Health
db_user = health_db.user
db_doc = health_db.doctor


