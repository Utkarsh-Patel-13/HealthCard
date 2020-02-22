import os
from flask import Flask, render_template, redirect, session, flash, send_file, request

from forms import RegistrationFormUser, LoginFormUser, EditUserForm
from model.models import Emergency, Address, User
from query.NewsQuery import find_latest_news
from query.UserQuery import create_user, find_user_by_id, get_user_aadhar, update_user
import json

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


@app.route('/report_patient')
def report_patient():
    currentUser = session.get('username')
    aadhar = get_user_aadhar(currentUser)
    location = os.path.join('/home/utkarsh/HealthServer/UserData/', aadhar)
    files = []

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
    return render_template('info_patient.html')
    #return render_template('Patient_home.html')


@app.route('/info_patient')
def info_patient():
    currentUser = session.get('username')
    patient = find_user_by_id(currentUser)

    if patient is not None:
        emergency_list = list(patient['EmergencyContact'].split(","))
        return render_template('info_patient.html', Name=patient['Name'], Email=patient['Email'],
                               Aadhar=patient['AadharNo'], Gender=patient['Gender'], DOB=patient['DOB'],
                               Contact=patient['ContactNo'], Address=patient['Address'],
                               e_Name=emergency_list[0], e_Rel=emergency_list[1], e_Contact=emergency_list[2])
    else:
        return render_template('info_patient.html')


@app.route('/edit_info_patient', methods=['GET', 'POST'])
def edit_info_patient():
    currentUser = session.get('username')
    user = find_user_by_id(currentUser)
    address_list = list(user['Address'].split(','))
    address = []
    for i in address_list:
        address.append(i.strip())
    emergency_list = list(user['EmergencyContact'].split(','))
    emergency = []
    for i in emergency_list:
        emergency.append(i.strip())
    form = EditUserForm()

    form.Name.data = user['Name']
    form.Gender.data = user['Gender']
    form.ContactNo.data = user['ContactNo']
    form.DOB.data = user['DOB']
    form.Street1.data = address[0]
    form.Street2.data = address[1]
    form.City.data = address[2]
    form.State.data = address[3]
    form.Zip.data = address[4]
    form.EmergencyContactName.data = emergency[0]
    form.EmergencyContactRelation.data = emergency[1]
    form.EmergencyContactNumber.data = emergency[2]

    if 'submit' in request.form:
        Name = request.form['Name']
        ContactNo = form.ContactNo.data = request.form['ContactNo']
        Gender = form.Gender.data = request.form['Gender']
        DOB = form.DOB.data = request.form['DOB']
        Street1 = form.Street1.data = request.form['Street1']
        Street2 = form.Street2.data = request.form['Street2']
        City = form.City.data = request.form['City']
        State = form.State.data = request.form['State']
        Zip = form.Zip.data = request.form['Zip']
        EmergencyContactName = form.EmergencyContactName.data = request.form['EmergencyContactName']
        EmergencyContactRelation = form.EmergencyContactRelation.data = request.form['EmergencyContactRelation']
        EmergencyContactNumber = form.EmergencyContactNumber.data = request.form['EmergencyContactNumber']

        if form.validate():
            user = update_user(Email=currentUser, Name=Name, ContactNo=ContactNo, Gender=Gender, DOB=DOB,
                               Street1=Street1, Street2=Street2, City=City, State=State, Zip=Zip,
                               EmergencyContactName=EmergencyContactName,
                               EmergencyContactRelation=EmergencyContactRelation,
                               EmergencyContactNumber=EmergencyContactNumber)

            return render_template('edit_info_patient.html', form=form, msg="Profile Updated Successfully")

    return render_template('edit_info_patient.html', form=form, msg="")


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
    news = find_latest_news()
    return render_template('currentnews.html', news=news)


@app.route('/Trending')
def Trending():
    news = find_latest_news()
    return render_template('user_cur_news.html', news=news)


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/index")


if __name__ == '__main__':
    app.run()
