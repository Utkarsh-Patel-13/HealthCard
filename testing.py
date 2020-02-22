from urllib.request import urlopen

from query.UserQuery import create_user, update_user
from query.DoctorQuery import create_doctor
from databaseConnections import db_user
from flask import Flask, request, render_template
from model.models import Address, Emergency
import requests
import urllib, json
from databaseConnections import db_user

"""
add = Address("13 Prabhupark Society", "Radhanpur Road", "Mehsana", "Gujarat", "384002")
emer = Emergency("Utkarsh", "Patel", "9586244772", "F")
user = create_user("Priyang", "something12@gmail.com", "2001-09-12", 'M', "9409481618", "888888888877", add, emer)
#user = create_doctor("Priyang", 'M', "9409481618", "123456789032", "111111")
print(user)
"""
"""
x = create_report("111111", "888888888888")
print(x)


#find_user_name("Priyang")
#update_user("123456789023", "9586244772")
"""

"""x = db_user.find()
for i in x:
    print(i['Email'])
"""
"""
URL = 'http://127.0.0.1:5000/edit_info_patient?csrf_token=IjZmMDVmMDNiN2ZlMDlhNDg1NjU0ZmZkZGM5Mzk5ODQzMTYzZGNiOTMi.XlCp9A.L3eBcnh4JYx3TjfyEAyqdAAXnF0&Name=Priyang+Patel&Gender=Male&ContactNo=9586244772&DOB=20%2F12%2F1999&Street1=13+Prabhupark+Society&Street2=Radhanpur+Road&City=Mehsana&State=Gujarat&Zip=384002&EmergencyContactName=Harshadbhai+Patel&EmergencyContactRelation=Father&EmergencyContactNumber=9979518938&submit=+Register+'

response = urlopen(URL)
data = json.loads(response.read())

print(data)
"""
Email = 'namra@gmail.com'
Name = 'ASD'
user = db_user.update_one({"Email": Email}, {"$set": {"Name": Name}})
print(user)