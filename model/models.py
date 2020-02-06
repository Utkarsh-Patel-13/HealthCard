from os.path import expanduser
import os
from extrafuncs import check_aadhar_validity, check_contact_validity


class Address():
    street1 = ""
    street2 = ""
    city = ""
    state = ""
    zip = ""

    def __init__(self, s1, s2, ct, st, zp):
        self.street1 = s1
        self.street2 = s2
        self.city = ct
        self.state = st
        self.zip = zp

    def __repr__(self):
        return '{}, {}, {}, {}, {}'.format(self.street1, self.street2, self.city, self.state, self.zip)


class Emergency():
    FirstName = ""
    LastName = ""
    ContactNo = ""
    Relation = ""

    def __init__(self, fname, lname, cno, rel):
        self.FirstName = fname
        self.LastName = lname
        self.ContactNo = cno
        self.Relation = rel

    def __repr__(self):
        return '{}, {}, {}, {}'.format(self.FirstName, self.LastName, self.ContactNo, self.Relation)


class User():
    # User Table

    Name = ""
    DOB = ""
    Gender = ''
    ContactNo = ""
    AadharNo = ""
    FileLoc = ""

    Address = ""
    EmergencyContact = ""

    def __init__(self, name, dob, gender, contact_no, aadhar_no, address, emergency):
        self.Name = name
        self.DOB = dob
        self.Gender = gender
        self.ContactNo = contact_no
        self.AadharNo = aadhar_no
        self.Address = address.__str__()
        self.EmergencyContact = emergency.__str__()

    def create_path_file(self):
        # create new file for user.
        home_path = expanduser("~")
        path_files_folder = os.path.join(home_path, "HealthServer", "PathFiles")
        user_path_file = os.path.join(path_files_folder, self.AadharNo + ".txt")

        if not os.path.exists(user_path_file):
            u_file = open(user_path_file, "w")
            self.FileLoc = user_path_file
            u_data_files_folder = self.create_user_folder()
            u_file.write(u_data_files_folder)
            u_file.close()

    def create_user_folder(self):
        # create data folder for user
        home_path = expanduser("~")
        folder_path = os.path.join(home_path, "HealthServer", "UserData")
        user_folder = folder_path + "/" + self.AadharNo
        if not (os.path.exists(user_folder)):
            os.mkdir(user_folder)

        basic_file_path = os.path.join(user_folder, self.AadharNo + "_basic.txt")
        self.create_basic_file(basic_file_path)
        return user_folder

    def check_validity(self):

        if check_contact_validity(self.ContactNo) == -1:
            return "ContactNumber invalid..."
        elif check_aadhar_validity(self.AadharNo) == -1:
            return "AadharNo invalid..."
        else:
            return "ok"

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


class Doctor():
    # Certificate Number verification left.

    CertificateNo = ""
    Name = ""
    Gender = ''
    AadharNo = ""
    ContactNo = ""
    # HospitalAddress = ""

    def __init__(self, name, gender, contact_no, aadhar_no, certificate_no):
        self.Name = name
        self.Gender = gender
        self.ContactNo = contact_no
        self.AadharNo = aadhar_no
        self.CertificateNo = certificate_no

    def check_lengths(self):
        if check_contact_validity(self.ContactNo) == -1:
            return "ContactNumber invalid..."
        elif check_aadhar_validity(self.AadharNo) == -1:
            return "AadharNo invalid..."
        else:
            return "ok"

