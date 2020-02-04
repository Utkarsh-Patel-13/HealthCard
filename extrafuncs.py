import re


def check_aadhar_validity(aadharNo):

    result = re.search('[\D]', aadharNo)

    if len(aadharNo) is not 12 or result is not None:
        return -1
    else:
        return 1


def check_contact_validity(contactNo):

    result = re.search('[\D]', contactNo)

    if len(contactNo) is not 10 or result is not None:
        return -1
    else:
        return 1
