import os
from flask import Flask, render_template, redirect, url_for, request, session, flash, send_file, jsonify

from forms import RegistrationFormUser, LoginFormUser
from model.models import Emergency, Address, User
from query.UserQuery import create_user, find_user_by_id, get_user_aadhar
import json
from databaseConnections import db_login, db_user

app = Flask(__name__)

app.config['SECRET_KEY'] = b'\xb0\xf4\xe8\\U\x8d\xba\xb4B2h\x88\xf9\x08\xb1J'

# client = MongoClient('localhost', 27017)


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
    currentUser = session.get('username')
    aadhar = get_user_aadhar(currentUser)
    location = os.path.join('/home/utkarsh/HealthServer/UserData/', aadhar)
    files = []

    # r=>root, d=>directories, f=>files
    for r, d, f in os.walk(location):
        for item in f:
            if '.pdf' in item:
                js = {'fname': item.__str__()}
                files.append(js)
    return render_template('report_patient.html', files=files)


@app.route('/return_files/<name>')
def return_files_tut(name):
    currentUser = session.get('username')
    try:
        aadhar = get_user_aadhar(currentUser)
        path = os.path.join('/home/utkarsh/HealthServer/UserData/', aadhar, name)
        return send_file(path, attachment_filename=name)
    except Exception as e:
        return str(e)


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


@app.route('/currentnews')
def currentnews():
    return render_template('currentnews.html')


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/index")


if __name__ == '__main__':
    app.run()
