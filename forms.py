from query.UserQuery import create_user, find_user_name, update_user
from query.DoctorQuery import create_doctor
from app import app, db_user
from flask import request, render_template
from validityfunctions import check_contact_validity, check_aadhar_validity, check_aadhar_in_DB
from model.models import Address, Emergency
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, ValidationError


class ReusableForm(Form):
    name = StringField('Name:', validators=[validators.required()])

    def validate_contactNo(self, contactNo):
        valid = check_contact_validity(contactNo)
        if valid == -1:
            raise ValidationError("Contact Number Invalid")

@app.route('/')
def index():
    return render_template('getAadhar.html')


@app.route('/', methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    if request.method == 'POST':
        if 'submit_aadhar' in request.form:
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

            if form.validate():
                return render_template('test.html', contact=contactNo, aadhar=aadharNo)
            else:
                return render_template('NewPatient.html', form=form)

        else:
            return render_template('test.html')


if __name__ == '__main__':
    app.run()

