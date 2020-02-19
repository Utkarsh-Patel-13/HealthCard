from os.path import expanduser
import os
from mongoengine import Document, StringField, IntField
from werkzeug.security import generate_password_hash, check_password_hash


class Address:

    def __init__(self, s1, s2, ct, st, zp):
        self.street1 = s1
        self.street2 = s2
        self.city = ct
        self.state = st
        self.zip = zp

    def __repr__(self):
        return '{}, {}, {}, {}, {}'.format(self.street1, self.street2, self.city, self.state, self.zip)


class Emergency:

    def __init__(self, name, cno, rel):
        self.Name = name
        self.ContactNo = cno
        self.Relation = rel

    def __repr__(self):
        return '{}, {}, {}'.format(self.Name, self.ContactNo, self.Relation)


class User(Document):
    # User Table
    Email = StringField(unique=True)
    Name = StringField()
    Password = StringField()
    Gender = StringField()
    ContactNo = StringField()
    AadharNo = StringField()
    DOB = StringField()
    Address = StringField()
    EmergencyContact = StringField()

    def create_user_folder(self):
        # create data folder for user
        home_path = expanduser("~")
        user_folder = os.path.join(home_path, "HealthServer", "UserData", self.AadharNo)
        if not (os.path.exists(user_folder)):
            os.mkdir(user_folder)

        basic_file_path = os.path.join(user_folder, self.AadharNo + "_basic.txt")
        self.create_basic_file(basic_file_path)
        return user_folder

    def set_password(self, password):
        self.Password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.Password, password)

    def create_basic_file(self, basic_file_path):
        u_basic_file = open(basic_file_path, "w")
        u_basic_file.write("I am %s \n\n\n" % self.Name)
        u_basic_file.write("Blood Group: \n")
        u_basic_file.write("Age: \n")
        u_basic_file.write("Height: \n")
        u_basic_file.write("Weight: \n")
        u_basic_file.write("Allergies: \n")
        u_basic_file.write("Special Notes: \n")
        u_basic_file.close()

    def _repr_(self):
        return '<User {}, {}, {}, {}>'.format(self.Name, self.DOB, self.Gender, self.AadharNo)


class Doctor:
    # Certificate Number verification left.

    def __init__(self, name, gender, contact_no, aadhar_no, certificate_no):
        self.Name = name
        self.Gender = gender
        self.ContactNo = contact_no
        self.AadharNo = aadhar_no
        self.CertificateNo = certificate_no

    def validity_check(self):
        if check_contact_validity(self.ContactNo) == -1:
            return "ContactNumber invalid..."
        elif check_aadhar_validity(self.AadharNo) == -1:
            return "AadharNo invalid..."
        else:
            return "ok"

