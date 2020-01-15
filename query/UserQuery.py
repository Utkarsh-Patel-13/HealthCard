import json
import pprint
from app import db, app
from model.models import User
from pymongo import errors
import hashlib
from ast import literal_eval


def perturb_hash(key, n):
    st = hash((key, n))
    temp = abs(st).__str__()
    return temp


def create_user(u_name, u_dob, u_gender, u_contact, u_aadhar):
    # creates new user in database
    new_user = User(u_name, u_dob, u_gender, u_contact, u_aadhar)

    check_str = new_user.check_lengths()
    if check_str == "ok":
        try:
            db.insert_one(new_user.__dict__)
            new_user.create_path_file()
            return new_user.Name + " created with Id " + new_user.Id
        except errors.DuplicateKeyError as e:
            return str("Duplicate Data........")
        except errors.PyMongoError as e:
            return str(e)
        except Exception as e:
            return str(e)
    else:
        print(check_str)
        return "Failed to create user"


def find_user_name():
    '''
        Work in progress...
        Find user in database.
    '''
    x = db.users.find_one({})
    print(x.__str__())
