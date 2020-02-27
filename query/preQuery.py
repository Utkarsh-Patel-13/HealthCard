from databaseConnections import db_pre
from model.models import Pre
from pymongo import errors


def create_pre(P1, P2, P3, P4, P5, D1, D2, D3, D4, D5, T1, T2, T3, T4, T5, preAadhar):
    # print(CertificateNo)
    # creates new user in database
    # emergency = Emergency(EmergencyContactName, EmergencyContactRelation, EmergencyContactNumber)
    # address = Address(Street1, Street2, City, State, Zip)
    new_pre = Pre(P1=P1, P2=P2, P3=P3, P4=P4, P5=P5, D1=D1, D2=D2, D3=D3, D4=D4, D5=D5, T1=T1, T2=T2, T3=T3, T4=T4, T5=T5, preAadhar=preAadhar)
    return new_pre
