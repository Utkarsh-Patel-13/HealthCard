from query.UserQuery import create_user, find_user_name, update_user
from query.DoctorQuery import create_doctor
from app import app, db_user
from flask import request, render_template
from extrafuncs import check_aadhar_validity
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


@app.route('/')
def index():
    return render_template('getAadhar.html')


@app.route('/', methods=["POST"])
def getvalue():
    if 'submit_aadhar' in request.form:
        aadharNo = request.form['aadhar']
        validity = check_aadhar_validity(aadharNo)
        print(aadharNo, validity)
        user = db_user.find_one({'AadharNo': aadharNo})

        if validity == -1:
            txt = "Invalid Aadhar Number..."
            return render_template('getAadhar.html', msg=txt)
        elif user is not None:
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
        zip = request.form['zip']

        e_fname = request.form['efirstname']
        e_lname = request.form['elastname']
        e_rel = request.form['relation']
        e_contact = request.form['econtact']

        name_list = [fname, mname, lname]
        name = ','.join(name_list)
        print(name)

        address_list = [street1, street2, city, state, zip]
        address = ','.join(address_list)
        print(address)

        return render_template('test.html', contact=contactNo, aadhar=aadharNo)

    else:
        return render_template('test.html')


if __name__ == '__main__':
    app.run()

"""
aadharNo = request.form['aadhar']
        fname = request.form['fname']
        mname = request.form['midname']
        lname = request.form['lastname']
        gender = request.form['gender']
        dob = request.form['DOB']
        conactNo = request.form['contactNo']

        street1 = request.form['street1']
        street2 = request.form['street2']
        city = request.form['city']
        state = request.form['state']
        zip = request.form['zip']

        address_list = [street1, street2, city, state, zip]
        address = ','.join(address_list)
        print(address)
"""