import re
from app import db_user


def check_aadhar_validity(aadharNo):
    # return -1 if aadhar is invalid
    result = re.search('[\D]', aadharNo)

    if len(aadharNo) is not 12 or result is not None:
        return -1
    else:
        return 1


def check_contact_validity(contactNo):
    # return -1 if contact number is invalid
    result = re.search('[\D]', contactNo)

    if len(contactNo) is not 10 or result is not None:
        return -1
    else:
        return 1

def check_aadhar_in_DB(aadharNo):
    valid = db_user.find_one({'AadharNo': aadharNo})
    if valid is not None:
        return 1
    else:
        return -1
