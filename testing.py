from query.UserQuery import create_user, find_user_name, update_user
from query.DoctorQuery import create_doctor
from databaseConnections import db_user
from flask import Flask, request, render_template
from validityfunctions import check_aadhar_validity, check_aadhar_in_DB
from model.models import Address, Emergency

"""
add = Address("13 Prabhupark Society", "Radhanpur Road", "Mehsana", "Gujarat", "384002")
emer = Emergency("Utkarsh", "Patel", "9586244772")
#user = create_user("Priyang", "2001-09-12", 'M', "9409481618", "123456789086", add, emer)
user = create_doctor("Priyang", 'M', "9409481618", "123456789032", "111111")
print(user)
"""

#find_user_name("Priyang")
#update_user("123456789023", "9586244772")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('getAadhar.html')


@app.route('/', methods=["POST"])
def getvalue():
    if 'submit_aadhar' in request.form:
        aadharNo = request.form['aadhar']
        validity = check_aadhar_validity(aadharNo)
        aadhar_exist = check_aadhar_in_DB(aadharNo)

        if validity == -1:
            txt = "Invalid Aadhar Number..."
            return render_template('getAadhar.html', msg=txt)
        elif aadhar_exist is not None:
            txt = "Aadhar already registered..."
            return render_template('getAadhar.html', msg=txt)
        else:
            return render_template('NewPatient.html', aadhar=aadharNo)

    elif 'submit_patient' in request.form:
        aadharNo = request.form['aadhar']
        fname = request.form['firstname']
        mname = request.form['midname']
        lname = request.form['lastname']
        gender = request.form['gender']
        dob = request.form['DOB']
        contactNo = request.form['contactNo']

        street1 = request.form['street1']
        street2 = request.form['street2']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip']

        e_fname = request.form['efirstname']
        e_lname = request.form['elastname']
        e_rel = request.form['relation']
        e_contact = request.form['econtact']

        name_list = [fname, mname, lname]
        u_name = ' '.join(name_list)

        address = Address(street1, street2, city, state, zip_code)
        emergency = Emergency(e_fname, e_lname, e_contact, e_rel)
        create_user(u_name, dob, gender, contactNo, aadharNo, address, emergency)

        return render_template('test.html', contact=contactNo, aadhar=aadharNo)

    else:
        return render_template('test.html')


if __name__ == '__main__':
    app.run()

