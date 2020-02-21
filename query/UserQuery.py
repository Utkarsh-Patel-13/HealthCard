from databaseConnections import db_user
from model.models import User, Address, Emergency
from pymongo import errors


def create_user(Email, Name, AadharNo, ContactNo, Gender, DOB, Street1, Street2,
                City, State, Zip, EmergencyContactName, EmergencyContactRelation, EmergencyContactNumber):
    # creates new user in database
    emergency = Emergency(EmergencyContactName, EmergencyContactRelation, EmergencyContactNumber)
    address = Address(Street1, Street2, City, State, Zip)
    new_user = User(Email=Email, Name=Name, AadharNo=AadharNo, ContactNo=ContactNo,
                    Gender=Gender, DOB=DOB, Address=address.__repr__(), EmergencyContact=emergency.__repr__())

    new_user.create_user_folder()

    return new_user


def find_user_by_id(u_id):
    user = db_user.find_one({'Email': u_id})
    return user


def get_user_aadhar(email):
    user = db_user.find_one({'Email': email})
    return user['AadharNo']


def update_user(uid, u_pno):
    db_user.update_one({'AadharNo': uid}, {"$set": {'ContactNo': u_pno}})


