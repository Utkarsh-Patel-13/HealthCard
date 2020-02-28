from databaseConnections import db_pp, db_lab
from model.models import Pp
from pymongo import errors


def create_Pp(AadharNo, BloodGroup, Age, Alergies, Weight, Height, Habits):
    new_pp = Pp(AadharNo=AadharNo, BloodGroup=BloodGroup, Age=Age, Alergies=Alergies, Weight=Weight, Height=Height, Habits=Habits)
    return new_pp

