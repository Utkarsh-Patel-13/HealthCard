import os

from bson import ObjectId
from flask import Flask, render_template, redirect, session, flash, send_file, request, url_for
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
from databaseConnections import db_user
from forms import RegistrationFormUser, LoginFormUser, EditUserForm, RegistrationFormDoctor, LoginFormDoctor, \
    SearchPatient, LoginFormLab, RegistrationFormLab, EntryFormPre, RegistrationFormMd, LoginFormMd
from model.models import Emergency, Address, User, Doctor, USER, Lab, Md
from query.DoctorQuery import create_doctor, find_doctor_by_id
from query.LabQuery import find_lab_by_id, create_lab
from query.MdQuery import create_md, find_user_by_Aadhar_M, find_md_by_id
from query.NewsQuery import find_latest_news
from query.UserQuery import create_user, find_user_by_id, get_user_aadhar, update_user, find_user_by_Aadhar, find_user
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from model.models import User
from query.preQuery import create_pre

app = Flask(__name__)
Bootstrap(app)
app.config['MONGO_URI'] = 'mongodb+srv://SPUM:srinking69@myhealthcard-1nsmr.mongodb.net/Health?retryWrites=true&w=majority'
mongo = PyMongo(app)

app.config['SECRET_KEY'] = b'\xb0\xf4\xe8\\U\x8d\xba\xb4B2h\x88\xf9\x08\xb1J'
UPLOAD_FOLDER = '/home/utkarsh/HealthServer/UserData/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# client = MongoClient('localhost', 27017)


ALLOWED_EXTENSIONS = {'pdf'}


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

AadharNo = None
currentLab = None

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@login_manager.user_loader
def load_user(user_id):
    return USER(find_user(user_id))


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
                           EmergencyContactNumber=EmergencyContactNumber, Reports=0)

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


@app.route('/login_patient', methods=["GET", "POST"])
def loginp():

    if session.get('username') is not None:
        Email = session.get('username')
        user = User.objects(Email=Email).first()
        name = user['Name']
        name = "".join(name.split())
        return redirect("/Patient/" + name.__str__())

    form = LoginFormUser()
    if form.validate_on_submit():
        Email = form.Email.data
        Password = form.Password.data
        try:
            user = User.objects(Email=Email).first()
            if user and user.get_password(Password):
                login_user(user, remember=True)
                session['username'] = user.Email
                name = user['Name']

                name = "".join(name.split())
                return redirect("/Patient/" + name.__str__())
            else:
                print("Incorrect username or password")
        except Exception as e:
            print(e)
    return render_template('login_patient.html', form=form)


@app.route('/Patient/<name>', methods=["GET", "POST"])
@login_required
def patient(name):
    return render_template('Patient.html')


@app.route('/Patient/Patient_home')
@login_required
def Patient_home():
    return render_template('Patient_home.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/report_patient')
@login_required
def report_patient():
    currentUser = session.get('username')
    global AadharNo
    aadhar = ""
    if currentUser is not None:
        aadhar = get_user_aadhar(currentUser)
    elif AadharNo is not None:
        aadhar = AadharNo

    # return render_template('report_patient.html', files=files)

    user = find_user_by_Aadhar(aadhar)
    r = user["Reports"]
    return render_template('report_patient.html', files=r)


@app.route('/return_files/<name>')
@login_required
def return_files_tut(name):
    try:
        currentUser = session.get('username')
        global AadharNo
        aadhar = ""
        if currentUser is not None:
            aadhar = get_user_aadhar(currentUser)
        elif AadharNo is not None:
            aadhar = AadharNo
        user = find_user_by_Aadhar(aadhar)
        filename = user['Rnames'][int(name)]
        return mongo.send_file(filename)
        #return send_file(path, attachment_filename=name)
    except Exception as e:
        return str(e)


@app.route('/info_patient')
@login_required
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
@login_required
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
        Name = form.Name.data = request.form['Name']
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


@app.route('/currentnews')
def currentnews():
    news = find_latest_news()
    return render_template('currentnews.html', news=news)


@app.route('/Trending')
@login_required
def Trending():
    news = find_latest_news()
    return render_template('user_cur_news.html', news=news)


@app.route('/newdoctor', methods=["GET", "POST"])
def newdoctor():
    if session.get('doctorname'):
        return redirect('/index')

    form = RegistrationFormDoctor()

    if form.validate_on_submit():
        Email = form.Email.data
        Password = form.Password.data
        AadharNo = form.AadharNo.data
        Name = form.Name.data
        ContactNo = form.ContactNo.data
        Gender = form.Gender.data
        CertificateNo = form.CertificateNo.data
        doctor = create_doctor(Email=Email, Name=Name, AadharNo=AadharNo,
                               ContactNo=ContactNo, Gender=Gender,
                               CertificateNo=CertificateNo)

        doctor.set_password(Password)

        try:
            doctor.save()
            flash("New ID Created Successfully", "success")
            return redirect("/login_doc")
        except Exception as e:
            flash("Failed to create user, try again")
            print(e)
            return redirect('/newdoctor')

    return render_template('newdoctor.html', form=form)


@app.route('/login_doc', methods=["GET", "POST"])
def logind():
    if session.get('doctorname'):
        Email = session.get('doctorname')
        doctor = Doctor.objects(Email=Email).first()
        name = doctor['Name']
        name = "".join(name.split())
        return redirect("/Doctor/" + name.__str__())

    form = LoginFormDoctor()
    if form.validate_on_submit():
        Email = form.Email.data
        Password = form.Password.data

        doctor = Doctor.objects(Email=Email).first()
        if doctor and doctor.get_password(Password):
            login_user(doctor, remember=True)
            session['doctorname'] = doctor.Email
            name = doctor['Name']
            name = "".join(name.split())
            return redirect("/Doctor/" + name.__str__())
        else:
            flash("Incorrect username or password")
    return render_template('login_doc.html', form=form)


@app.route('/Doctor/<name>', methods=["GET", "POST"])
@login_required
def doctor(name):
    form = SearchPatient()
    if form.validate_on_submit():
        global AadharNo
        AadharNo = form.AadharNo.data
        return redirect('/doctor_w_patient')
    return render_template('DOCTOR.html', form=form)


@app.route('/doctor_home')
@login_required
def doctor_home():
    return render_template('doctor_home.html')


@app.route('/doctor_info')
@login_required
def doctor_info():
    currentDoctor = session.get('doctorname')
    doctor = find_doctor_by_id(currentDoctor)
    if doctor is not None:
        return render_template('doctor_info.html', Name=doctor['Name'], Email=doctor['Email'],
                               Aadhar=doctor['AadharNo'], Gender=doctor['Gender'],CertificateNo=doctor['CertificateNo'])
    else:
        return render_template('doctor_info.html')


@app.route('/doctor_w_patient')
@login_required
def doctor_w_patient():
    return render_template('doctor_w_patient.html')


@app.route('/info_patient_by_doctor')
@login_required
def info_patient_by_doctor():
    patient = find_user_by_Aadhar(AadharNo)
    if patient is not None:
        emergency_list = list(patient['EmergencyContact'].split(","))
        return render_template('info_patient.html', Name=patient['Name'], Email=patient['Email'],
                               Aadhar=patient['AadharNo'], Gender=patient['Gender'], DOB=patient['DOB'],
                               Contact=patient['ContactNo'], Address=patient['Address'],
                               e_Name=emergency_list[0], e_Rel=emergency_list[1], e_Contact=emergency_list[2])
    else:
        return render_template('info_patient.html')


@app.route('/upload_report', methods=['GET', 'POST'])
@login_required
def upload_report():
    currentUser = session.get('username')
    global AadharNo
    aadhar = ""
    if currentUser is not None:
        aadhar = get_user_aadhar(currentUser)
    elif AadharNo is not None:
        aadhar = AadharNo

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.filename = aadhar + "-" + file.filename
            filename = secure_filename(file.filename)
            mongo.save_file(filename, file)

            user = find_user_by_Aadhar(aadhar)
            reports = user["Reports"]
            reports = reports + 1
            user["Rnames"].append(file.filename)
            db_user.update_one({"AadharNo": aadhar}, {"$set": {"Reports": reports, "Rnames": user['Rnames']}})

            return render_template('upload_report.html')
    return render_template('upload_report.html')


@app.route('/newlab', methods=["GET", "POST"])
def newlab():
    if session.get('labname'):
        return redirect('/index')

    form = RegistrationFormLab()

    if form.validate_on_submit():
        Email = form.Email.data
        Password = form.Password.data
        AadharNo = form.AadharNo.data
        Name = form.Name.data
        ContactNo = form.ContactNo.data
        lab = create_lab(Email=Email, Name=Name, AadharNo=AadharNo,
                         ContactNo=ContactNo)

        lab.set_password(Password)

        try:
            lab.save()
            flash("New ID Created Successfully", "success")
            return redirect("/login_lab")
        except Exception as e:
            flash("Failed to create user, try again")
            print(e)
            return redirect('/newlab')

    return render_template('newlab.html', form=form)


@app.route('/login_lab', methods=["GET", "POST"])
def loginlab():
    if session.get('labname'):
        Email = session.get('labname')
        user = User.objects(Email=Email).first()
        name = user['Name']
        name = "".join(name.split())
        return redirect("/Lab/" + name.__str__())

    form = LoginFormLab()
    if form.validate_on_submit():
        Email = form.Email.data
        Password = form.Password.data

        try:
            lab = Lab.objects(Email=Email).first()
            print(lab)
            if lab and lab.get_password(Password):
                login_user(lab, remember=True)
                print("asd")
                session['labname'] = lab.Email
                name = lab['Name']
                print(name)
                name = "".join(name.split())
                return redirect("/Lab/" + name.__str__())
            else:
                print("Incorrect username or password")
        except Exception as e:
            print(e)
    return render_template('login_lab.html', form=form)


@app.route('/Lab/<name>', methods=["GET", "POST"])
@login_required
def lab(name):
    form = SearchPatient()
    if form.validate_on_submit():
        global AadharNo
        AadharNo = form.AadharNo.data
        return redirect('/lab_w_patient')
    return render_template('Lab.html', form=form)


@app.route('/lab_info')
@login_required
def lab_info():
    currentlab = session.get('labname')
    lab = find_lab_by_id(currentlab)
    if lab is not None:
        return render_template('lab_info.html', Name=lab['Name'], Email=lab['Email'],
                               Aadhar=lab['AadharNo'])
    else:
        return render_template('lab_info.html')


@app.route('/lab_w_patient')
@login_required
def lab_w_patient():
    return render_template('lab_w_patient.html')


@app.route('/info_patient_by_lab')
@login_required
def info_patient_by_lab():
    global AadharNo
    patient = find_user_by_Aadhar(AadharNo)
    if patient is not None:
        emergency_list = list(patient['EmergencyContact'].split(","))
        return render_template('info_patient.html', Name=patient['Name'], Email=patient['Email'],
                               Aadhar=patient['AadharNo'], Gender=patient['Gender'], DOB=patient['DOB'],
                               Contact=patient['ContactNo'], Address=patient['Address'],
                               e_Name=emergency_list[0], e_Rel=emergency_list[1], e_Contact=emergency_list[2])
    else:
        return render_template('info_patient.html')


@app.route("/precautions", methods=["GET", "POST"])
def upload_pre():
    global AadharNo
    form = EntryFormPre()

    if form.is_submitted():
        P1 = form.P1.data
        P2 = form.P2.data
        P3 = form.P3.data
        P4 = form.P4.data
        P5 = form.P5.data
        D1 = form.D1.data
        D2 = form.D2.data
        D3 = form.D3.data
        D4 = form.D4.data
        D5 = form.D5.data
        T1 = form.T1.data
        T2 = form.T2.data
        T3 = form.T3.data
        T4 = form.T4.data
        T5 = form.T5.data

        pre = create_pre(P1=P1, P2=P2, P3=P3, P4=P4, P5=P5, D1=D1, D2=D2, D3=D3, D4=D4, D5=D5, T1=T1, T2=T2, T3=T3,
                         T4=T4, T5=T5, preAadhar=AadharNo)
        try:
            pre.save()
            flash("New ID Created Successfully", "success")
            return render_template("upload_pre.html", form=form)
        except Exception as e:
            flash("Failed to create user, try again")
            print(e)
            return render_template('upload_pre.html', form=form)
    return render_template('upload_pre.html', form=form)


@app.route('/newmd', methods=["GET", "POST"])
def newmd():
    if session.get('mdname'):
        return redirect('/index')

    form = RegistrationFormMd()

    if form.validate_on_submit():
        Email = form.Email.data
        Password = form.Password.data
        AadharNo = form.AadharNo.data
        Name = form.Name.data
        ContactNo = form.ContactNo.data
        md = create_md(Email=Email, Name=Name, AadharNo=AadharNo,
                       ContactNo=ContactNo)

        md.set_password(Password)

        try:
            md.save()
            flash("New ID Created Successfully", "success")
            return redirect("/loginmd")
        except Exception as e:
            flash("Failed to create user, try again")
            print(e)
            return redirect('/newmedical')

    return render_template('newmedical.html', form=form)


@app.route('/loginmd', methods=["GET", "POST"])
def loginmd():
    if session.get('mdname'):
        Email = session.get('mdname')
        md = Md.objects(Email=Email).first()
        name = md['Name']
        name = "".join(name.split())
        return redirect("/Medical")

    form = LoginFormMd()
    if form.validate_on_submit():
        Email = form.Email.data
        Password = form.Password.data

        md = Md.objects(Email=Email).first()
        if md and md.get_password(Password):
            login_user(md, remember=True)
            session['mdname'] = md.Email
            name = md['Name']
            name = "".join(name.split())
            return redirect("/Medical")
        else:
            flash("Incorrect username or password")
    return render_template('loginmd.html', form=form)


@app.route('/Medical', methods=["GET", "POST"])
def Medical():
    form = SearchPatient()
    if form.validate_on_submit():
        global AadharNo
        AadharNo = form.AadharNo.data
        return redirect('md_w_patient')
    return render_template('Medical.html', form=form)


@app.route('/md_info')
def md_info():
    currentMd = session.get('mdname')
    md = find_md_by_id(currentMd)
    print(md)
    if md is not None:
        return render_template('md_info.html', Name=md['Name'], Email=md['Email'],
                               Aadhar=md['AadharNo'])
    else:
        return render_template('md_info.html')


@app.route('/md_w_patient')
def md_w_patient():
    return render_template('md_w_patient.html')


@app.route('/view_pre')
def view_pre():
    global AadharNo
    patientM = find_user_by_Aadhar_M(AadharNo)
    if patientM is not None:
        return render_template('view_pre.html', P1=patientM['P1'], P2=patientM['P2'], P3=patientM['P3'],
                               P4=patientM['P4'], P5=patientM['P5'],
                               D1=patientM['D1'], D2=patientM['D2'], D3=patientM['D3'], D4=patientM['D4'],
                               D5=patientM['D5'],
                               T1=patientM['T1'], T2=patientM['T2'], T3=patientM['T3'], T4=patientM['T4'],
                               T5=patientM['T5'])
    else:
        return render_template('view_pre.html')


@app.route('/info_patient_by_md')
def info_patient_by_md():
    global AadharNo
    patient = find_user_by_Aadhar(AadharNo)
    if patient is not None:
        emergency_list = list(patient['EmergencyContact'].split(","))
        return render_template('info_patient.html', Name=patient['Name'], Email=patient['Email'],
                               Aadhar=patient['AadharNo'], Gender=patient['Gender'], DOB=patient['DOB'],
                               Contact=patient['ContactNo'], Address=patient['Address'],
                               e_Name=emergency_list[0], e_Rel=emergency_list[1], e_Contact=emergency_list[2])
    else:
        return render_template('info_patient.html')


@app.route("/logout")
@login_required
def logout():
    if session.get('username') is not None:
        session.pop('username')
    if session.get('doctorname') is not None:
        session.pop('doctorname')
    if session.get('labname') is not None:
        session.pop('labname')
    if session.get('mdname') is not None:
        session.pop('mdname')
    logout_user()
    return redirect("/index")


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1",
            port=9000,
            threaded=True)


