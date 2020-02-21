from pymongo import MongoClient
from mongoengine import connect
import dns

client = MongoClient("mongodb+srv://SPUM:srinking69@myhealthcard-1nsmr.mongodb.net/Health?retryWrites=true&w=majority")

engine_client = connect("Health",
                        host="mongodb+srv://SPUM:srinking69@myhealthcard-1nsmr.mongodb.net/Health?retryWrites=true&w=majority")

user_col = engine_client['user']

health_db = client.Health
db_user = health_db.user
db_doc = health_db.doctor
db_login = health_db.login
