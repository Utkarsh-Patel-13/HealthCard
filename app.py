import os
from flask import Flask, render_template, redirect, url_for, request
import pdfkit
from model.models import Emergency, Address
from query.UserQuery import create_user
from validityfunctions import check_aadhar_validity, check_aadhar_in_DB
from databaseConnections import db_login, db_user

app = Flask(__name__)

# client = MongoClient('localhost', 27017)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def index():
    if 'sign_up' in request.form:
        return redirect(url_for('getAadhar'))
    if 'sign_in' in request.form:
        return redirect(url_for('login'))
    if 'pdf' in request.form:
        return redirect(url_for('report'))

    return render_template('home.html')


@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':

        try:
            aadhar = request.form['aadhar']
            uname = request.form['u_name']
            uage = request.form['u_age']
            dname = request.form['d_name']
            cause = request.form['cause']
            med = request.form['med']
            notes = request.form['notes']

            file = open('tmp.txt', 'w')

            file.write("Aadhar : %s \n\n" % aadhar)
            file.write("Name : %s \n\n" % uname)
            file.write("Age : %s \n\n\n" % uage)
            file.write("Doctor Name : %s \n\n\n\n" % dname)
            file.write("Cause : \n\n %s \n\n\n" % cause)
            file.write("Medications : \n\n %s \n\n\n" % med)
            file.write("Notes : \n\n %s \n\n" % notes)

            file.close()

            pdfkit.from_file('tmp.txt', 'patient.pdf')

            os.remove('tmp.txt')

        except Exception as e:
            print(e.__str__())

        return render_template('test.html')

    return render_template('report.html')


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
            txt = "Aadhar already registered..."
            return render_template('getAadhar.html', msg=txt)
        else:
            return redirect(url_for("newPatient"))

    return render_template('getAadhar.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        valid = False

        user = db_login.find_one({'username': username})
        if user is not None:
            if password == user['password']:
                valid = True

        if user is not None and valid is True:
            try:
                user = db_user.find_one({'Email': username})

                aadhar = user['AadharNo']
                name = user['Name']
                email = user['Email']
                dob = user['DOB']
                gender = user['Gender']
                contact = user['ContactNo']
                address = user['Address']

                print(user.__str__())

                return render_template('userProfile.html', aadhar=aadhar, name=name, email=email, dob=dob,
                                       gender=gender,
                                       contact=contact, address=address)
            except Exception as e:
                print(e.__str__())


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
        email = request.form['email']
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
        create_user(u_name, email, dob, gender, contactNo, aadharNo, address, emergency)

        return render_template('test.html', contact=contactNo, aadhar=aadharNo)

    return render_template("NewPatient.html")


if __name__ == '__main__':
    app.run()
