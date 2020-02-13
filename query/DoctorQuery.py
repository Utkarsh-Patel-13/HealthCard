from databaseConnections import db_doc
from model.models import Doctor
from pymongo import errors


def create_doctor(u_name, u_gender, u_contact, u_aadhar, u_certificate):
    # creates new user in database
    new_doc = Doctor(u_name, u_gender, u_contact, u_aadhar, u_certificate)

    check_str = new_doc.check_lengths()
    if check_str == "ok":
        try:
            db_doc.insert_one(new_doc.__dict__)
            # new_doc.create_path_file()
            return new_doc.Name + " created with Id " + new_doc.AadharNo
        except errors.DuplicateKeyError as e:
            return str("Duplicate Data........")
        except errors.PyMongoError as e:
            return str(e)
        except Exception as e:
            return str(e)
    else:
        print(check_str)
        return "Failed to create user"
