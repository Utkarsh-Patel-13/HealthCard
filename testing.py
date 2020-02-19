from query.UserQuery import create_user, find_user_name, update_user
from query.DoctorQuery import create_doctor
from databaseConnections import db_user
from flask import Flask, request, render_template
from validityfunctions import check_aadhar_validity, check_aadhar_in_DB
from model.models import Address, Emergency
from query.UserData import create_report

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

x = db_user.find()
for i in x:
    print(i['Email'])
