import os
from flask import Flask, render_template, redirect, url_for, request, session, flash

from forms import RegistrationFormUser, LoginFormUser
from model.models import Emergency, Address, User
from query.UserQuery import create_user, find_user_by_id
from databaseConnections import db_login, db_user

app = Flask(__name__)

app.config['SECRET_KEY'] = b'\xb0\xf4\xe8\\U\x8d\xba\xb4B2h\x88\xf9\x08\xb1J'

# client = MongoClient('localhost', 27017)

currentUser = None


@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/newpatient', methods=["GET", "POST"])
def newpatient():
    if session.get('username'):
        return redirect('/index')

    form = RegistrationFormUser()

    if form.validate_on_submit():
        Email = form.Email.data
        Password = form.Password.data
        AadharNo = form.AadharNo.data
        Name = form.Name.data
        ContactNo = form.ContactNo.data
        Gender = form.Gender.data
        DOB = form.DOB.data
        Street1 = form.Street1.data
        Street2 = form.Street2.data
        City = form.City.data
        State = form.State.data
        Zip = form.Zip.data
        EmergencyContactName = form.EmergencyContactName.data
        EmergencyContactRelation = form.EmergencyContactRelation.data
        EmergencyContactNumber = form.EmergencyContactNumber.data

        user = create_user(Email=Email, Name=Name, AadharNo=AadharNo,
                           ContactNo=ContactNo, Gender=Gender, DOB=DOB,
                           Street1=Street1, Street2=Street2, City=City, State=State, Zip=Zip,
                           EmergencyContactName=EmergencyContactName, EmergencyContactRelation=EmergencyContactRelation,
                           EmergencyContactNumber=EmergencyContactNumber)

        user.set_password(Password)

        try:
            user.save()
            flash("New ID Created Successfully", "success")
            return redirect("/login_patient")
        except Exception as e:
            flash("Failed to create user, try again")
            print(e)
            return redirect('/newpatient')

    return render_template('newpatient.html', form=form)


@app.route('/newdoctor')
def newdoctor():
    return render_template('newdoctor.html')


@app.route('/login_doc')
def logind():
    return render_template('login_doc.html')


@app.route('/login_patient', methods=["GET", "POST"])
def loginp():
    if session.get('username'):
        return redirect("/Patient")

    form = LoginFormUser()
    if form.validate_on_submit():
        Email = form.Email.data
        global currentUser
        currentUser = Email
        print(Email, " ", currentUser)
        Password = form.Password.data

        user = User.objects(Email=Email).first()
        if user and user.get_password(Password):
            # session['user_id'] = user.user_id
            session['username'] = user.Email
            return redirect("/Patient")
        else:
            flash("Incorrect username or password")
    return render_template('login_patient.html', form=form)


@app.route('/Doctor', methods=["GET", "POST"])
def doctor():
    return render_template('DOCTOR.html')


@app.route('/Patient', methods=["GET", "POST"])
def patient():
    return render_template('Patient.html')



@app.route('/upload_report')
def upload_report():
    return render_template('upload_report.html')


@app.route('/Trending')
def Trending():
    return render_template('Trending.html')


@app.route('/report_patient')
def report_patient():
    x = [1, 2, 3, 4, 5]
    return render_template('report_patient.html', x=x)


@app.route('/Patient_home')
def Patient_home():
    return render_template('Patient_home.html')


@app.route('/info_patient')
def info_patient():
    global currentUser
    patient = find_user_by_id(currentUser)

    if patient is not None:
        emergency_list = list(patient['EmergencyContact'].split(","))
        return render_template('info_patient.html', Name=patient['Name'], Email=patient['Email'],
                               Aadhar=patient['AadharNo'], Gender=patient['Gender'], DOB=patient['DOB'],
                               Contact=patient['ContactNo'], Address=patient['Address'],
                               e_Name=emergency_list[0], e_Rel=emergency_list[1], e_Contact=emergency_list[2])
    else:
        return render_template('info_patient.html')


@app.route('/edit_info_patient')
def edit_info_patient():
    return render_template('edit_info_patient.html')


@app.route('/doctor_w_patient')
def doctor_w_patient():
    return render_template('doctor_w_patient.html')


@app.route('/doctor_info')
def doctor_info():
    return render_template('doctor_info.html')


@app.route('/doctor_home')
def doctor_home():
    return render_template('doctor_home.html')


@app.route('/DOC_1st')
def DOC_1st():
    return render_template('DOC_1st.html')


@app.route('/currentnews')
def currentnews():
    return render_template('currentnews.html')


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/index")



"""
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
"""

if __name__ == '__main__':
    app.run()
