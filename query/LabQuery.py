from databaseConnections import db_lab
from model.models import Lab
from pymongo import errors


def create_lab(Email, Name, AadharNo, ContactNo):
    new_lab = Lab(Email=Email, Name=Name, AadharNo=AadharNo, ContactNo=ContactNo)
    return new_lab

def find_lab_by_id(u_id):

    print(u_id)
    lab = db_lab.find_one({"Email": u_id})
    print(lab)
    return lab