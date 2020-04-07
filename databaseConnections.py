from pymongo import MongoClient
from mongoengine import connect
import dns

client = MongoClient("mongodb+srv://SPUM:--------@myhealthcard-1nsmr.mongodb.net/Health?retryWrites=true&w=majority")

engine_client = connect("Health",
                        host="mongodb+srv://SPUM:--------@myhealthcard-1nsmr.mongodb.net/Health?retryWrites=true&w=majority")

user_col = engine_client['user']

health_db = client.Health
db_user = health_db.user
db_doc = health_db.doctor
db_news = health_db.News
db_lab = health_db.lab
db_pre=health_db.pre
db_md=health_db.md
db_qr = health_db.qr
db_pp=health_db.pp
