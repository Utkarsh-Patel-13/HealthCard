import hashlib
from os.path import expanduser
import os
from mongoengine import Document, StringField, IntField, ListField
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

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


class User(UserMixin, Document):
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
    Reports = IntField()
    Rnames = ListField()

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
        result = hashlib.sha256(password.encode())
        self.Password = result.hexdigest()

    def get_password(self, password):
        result = hashlib.sha256(password.encode())
        password = result.hexdigest()
        if self.Password == password:
            return True
        else:
            return False

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


class Doctor(UserMixin, Document):
    # Certificate Number verification left.
    Email = StringField(unique=True)
    Name = StringField()
    Password = StringField()
    Gender = StringField()
    ContactNo = StringField()
    AadharNo = StringField()
    CertificateNo = StringField()

    def set_password(self, password):
        result = hashlib.sha256(password.encode())
        self.Password = result.hexdigest()

    def get_password(self, password):
        result = hashlib.sha256(password.encode())
        password = result.hexdigest()
        if self.Password == password:
            return True
        else:
            return False


class News:
    title = ""
    guid = ""
    description = ""


class SearchPatient():
    AadharNo = StringField()


class USER(UserMixin):
    def __init__(self, user_json):
        self.user_json = user_json

    def get_id(self):
        print(self.user_json)
        object_id = self.user_json.get('_id')
        return str(object_id)


