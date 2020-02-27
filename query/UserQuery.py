from bson import ObjectId

from databaseConnections import db_user
from model.models import User, Address, Emergency
from pymongo import errors


def create_user(Email, Name, AadharNo, ContactNo, Gender, DOB, Street1, Street2,
                City, State, Zip, EmergencyContactName, EmergencyContactRelation, EmergencyContactNumber, Reports):
    # creates new user in database
    emergency = Emergency(EmergencyContactName, EmergencyContactRelation, EmergencyContactNumber)
    address = Address(Street1, Street2, City, State, Zip)
    new_user = User(Email=Email, Name=Name, AadharNo=AadharNo, ContactNo=ContactNo,
                    Gender=Gender, DOB=DOB, Address=address.__repr__(), EmergencyContact=emergency.__repr__(),
                    Reports=Reports)


    new_user.create_user_folder()

    return new_user


def update_user(Email, Name, ContactNo, Gender, DOB,
                Street1, Street2, City, State, Zip,
                EmergencyContactName, EmergencyContactRelation, EmergencyContactNumber, Reports):

    la = [Street1, Street2, City, State, Zip]
    le = [EmergencyContactName, EmergencyContactRelation, EmergencyContactNumber]
    address = ','.join(la)
    emergency = ','.join(le)
    try:
        user = db_user.update_one({"Email": Email}, {"$set": {"Name": Name, "ContactNo": ContactNo, "Gender": Gender,
                                                              "DOB": DOB, "Address": address,
                                                              "EmergencyContact": emergency, "Reports": Reports}})
        return user
    except Exception as e:
        print(e)
        return e.__str__()


def find_user_by_id(u_id):
    user = db_user.find_one({'Email': u_id})
    return user


def find_user(u_id):
    user = db_user.find_one({'_id': u_id})
    return user


def get_user_aadhar(email):
    user = db_user.find_one({'Email': email})
    return user['AadharNo']


def find_user_by_Aadhar(u_id):
    user = db_user.find_one({'AadharNo': u_id})
    return user