from flask import Flask, render_template, redirect, url_for, request
import dns

from model.models import Emergency, Address
from query.UserQuery import create_user
from validityfunctions import check_aadhar_validity, check_aadhar_in_DB
from databaseConnections import db_login


app = Flask(__name__)

# client = MongoClient('localhost', 27017)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def index():
    if 'sign_up' in request.form:
        return redirect(url_for('getAadhar'))
    if 'sign_in' in request.form:
        return redirect(url_for('login'))

    return render_template('home.html')


@app.route('/getAadhar', methods=['GET', 'POST'])
def getAadhar():
    if request.method == 'POST':
        aadharNo = request.form['aadhar']
        validity = check_aadhar_validity(aadharNo)
        aadhar_exist = check_aadhar_in_DB(aadharNo)

        if validity == -1:
            txt = "Invalid Aadhar Number..."
            return render_template('getAadhar.html', msg=txt)
        elif aadhar_exist == 1:
            print(aadhar_exist)
            txt = "Aadhar already registered..."
            return render_template('getAadhar.html', msg=txt)
        else:
            return redirect(url_for("newPatient"))

    return render_template('getAadhar.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        valid = False

        user = db_login.find_one({'username': username})
        if user is not None:
            if password == user['password']:
                valid = True

        if user is not None and valid is True:
            return render_template('test.html')
        else:
            return render_template('login.html', error="Username/Password Incorrect")

    return render_template('login.html')


@app.route('/newPatient', methods=['GET', 'POST'])
def newPatient():
    if request.method == 'POST':
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

    return render_template("NewPatient.html")

"""

@app.route('/getAadhar/NewPatient', methods=['POST'])
def new_user():
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
"""

if __name__ == '__main__':
    app.run()
