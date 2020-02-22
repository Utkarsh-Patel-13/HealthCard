from databaseConnections import db_doc
from model.models import Doctor
from pymongo import errors


def create_doctor(Email, Name, AadharNo, ContactNo, Gender,CertificateNo):
    print(CertificateNo)
    # creates new user in database
    # emergency = Emergency(EmergencyContactName, EmergencyContactRelation, EmergencyContactNumber)
    # address = Address(Street1, Street2, City, State, Zip)
    new_doctor = Doctor(Email=Email, Name=Name, AadharNo=AadharNo, ContactNo=ContactNo,
                        Gender=Gender, CertificateNo=CertificateNo)
    return new_doctor


def find_doctor_by_id(u_id):

    doctor = db_doc.find_one({'Email': u_id})
    return doctor
