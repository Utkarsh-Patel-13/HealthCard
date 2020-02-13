from databaseConnections import db_user
from model.models import User
from pymongo import errors


def create_user(u_name, u_dob, u_gender, u_contact, u_aadhar, u_address, u_emergency):
    # creates new user in database
    new_user = User(u_name, u_dob, u_gender, u_contact, u_aadhar, u_address, u_emergency)

    # TODO: raise exception if user not created, return user_id if user created successfully.

    check_str = new_user.check_validity()
    if check_str == "ok":
        try:
            db_user.insert_one(new_user.__dict__)
            new_user.create_path_file()
            return new_user.Name + " created with Id " + new_user.AadharNo
        except errors.DuplicateKeyError as e:
            return str("Duplicate Data........")
        except errors.PyMongoError as e:
            return str(e)
        except Exception as e:
            return str(e)
    else:
        print(check_str)
        return "Failed to create user"


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
    user = db_user.find_one({'AadharNo': u_id})
    print(user.__str__())
    return user


def update_user(uid, u_pno):
    db_user.update_one({'AadharNo': uid}, {"$set": {'ContactNo': u_pno}})


