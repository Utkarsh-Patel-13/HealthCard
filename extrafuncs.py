import re


def check_aadhar_validity(aadharNo):

    result = re.search('[\D]', aadharNo)

    if len(aadharNo) is not 12 or result is not None:
        return -1
    else:
        return 0

