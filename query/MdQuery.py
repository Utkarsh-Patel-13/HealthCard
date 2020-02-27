from databaseConnections import db_md, db_pre
from model.models import Md
from pymongo import errors


def create_md(Email, Name, AadharNo, ContactNo):
    new_md = Md(Email=Email, Name=Name, AadharNo=AadharNo, ContactNo=ContactNo)
    return new_md


def find_md_by_id(u_id):
    print(u_id)
    md = db_md.find_one({"Email": u_id})
    print(md)
    return md


def find_user_by_Aadhar_M(u_id):
    print(u_id + " hello")
    pre = db_pre.find_one({'preAadhar': u_id})
    print(pre)
    return pre