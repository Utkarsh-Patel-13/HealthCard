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


# TODO: Improving finding functions


def find_user_name(u_name):

    '''
        Work in progress...
        Find user in database.
    '''

    try:
        user = db_user.find_one({'Name': u_name})
        print(user.__str__())
    except Exception as e:
        print(e.__str__())


def find_user_by_id(u_id):
    '''
        Work in progress...
        Find user in database by AadharNo.
    '''
    user = db_user.find_one({'Email': u_id})
    print(user.__str__())
    return user


def update_user(uid, u_pno):
    db_user.update_one({'AadharNo': uid}, {"$set": {'ContactNo': u_pno}})


