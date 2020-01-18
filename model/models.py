from os.path import expanduser
import os
from app import db


class User():
    #User Table

    Id = ""
    Name = ""
    DOB = ""
    Gender = ''
    ContactNo = ""
    AadharNo = ""
    FileLoc = ""

    def __init__(self, Name, DOB, Gender, ContactNo, AadharNo):
        self.Name = Name
        self.DOB = DOB
        self.Gender = Gender
        self.ContactNo = ContactNo
        self.AadharNo = AadharNo
        self.__hash__()

    def create_path_file(self):
        # create new file for user.
        home_path = expanduser("~")
        path_files_folder = os.path.join(home_path, "HealthServer", "PathFiles")
        user_path_file = os.path.join(path_files_folder, self.Id + ".txt")

        if not os.path.exists(user_path_file):
            u_file = open(user_path_file, "w")
            self.FileLoc = user_path_file
            u_data_files_folder = self.create_user_folder()
            u_file.write(u_data_files_folder)
            u_file.close()

    def create_user_folder(self):
        #create data folder for user
        home_path = expanduser("~")
        folder_path = os.path.join(home_path, "HealthServer", "UserData")
        user_folder = folder_path + "/" + self.Id
        if not (os.path.exists(user_folder)):
            os.mkdir(user_folder)

        basic_file_path = os.path.join(user_folder, self.Id + "_basic.txt")
        u_file = open(basic_file_path, "w")
        u_file.write("I am %s \n" % self.Id)
        u_file.close()
        return user_folder

    def check_lengths(self):
        if len(self.ContactNo) != 10:
            return "ContactNumber invalid..."
        elif len(self.AadharNo) != 12:
            return "AadharNo invalid..."
        else:
            return "ok"

    def __hash__(self):
        self.Id = hash((self.Name, self.ContactNo, self.AadharNo))
        self.Id = abs(self.Id).__str__()

    def _repr_(self):
        return '<User {}, {}, {}, {}, {}>'.format(self.Id, self.Name, self.DOB, self.Gender, self.AadharNo)