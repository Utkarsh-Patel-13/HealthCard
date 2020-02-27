from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField , SubmitField, BooleanField, IntegerField,TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from model.models import User


class LoginFormUser(FlaskForm):
    Email = StringField("Email",validators=[DataRequired(), Email()])
    Password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=15)])
    submit = SubmitField("Login")


class RegistrationFormUser(FlaskForm):
    Email = StringField("Email", validators=[DataRequired(), Email()])
    Password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=15)])
    Password_confirm = PasswordField("Confirm Password",
                                     validators=[DataRequired(), Length(min=6, max=15), EqualTo('Password')])
    Name = StringField("Name", validators=[DataRequired(), Length(min=2, max=55)])
    Gender = StringField("Gender", validators=[DataRequired(), Length(min=2, max=55)])
    ContactNo = StringField("Contact",
                             validators=[DataRequired(), Length(min=10, max=13)])
    AadharNo = StringField("Aadhar", validators=[DataRequired(), Length(min=12, max=12)])
    DOB = StringField("DOB", validators=[DataRequired(), Length(min=2, max=55)])
    Street1 = StringField("Street Address Line 1", validators=[DataRequired()])
    Street2 = StringField("Street Address Line 2", validators=[DataRequired()])
    City = StringField("City", validators=[DataRequired()])
    State = StringField("State", validators=[DataRequired()])
    Zip = StringField("Zip Code", validators=[Length(min=6, max=6)])
    EmergencyContactName = StringField("Emergency contact Full Name", validators=[DataRequired()])
    EmergencyContactRelation = StringField("Emergency contact Relation", validators=[DataRequired()])
    EmergencyContactNumber = StringField("Emergency contact PhoneNo", validators=[DataRequired()])
    submit = SubmitField(" Register ")

    def validate_Email(self, Email):
        user = User.objects(Email=Email.data).first()
        if user:
            raise ValidationError("Email Exists")


class EditUserForm(FlaskForm):
    Name = StringField("Name", validators=[DataRequired(), Length(min=2, max=55)])
    Gender = StringField("Gender", validators=[DataRequired(), Length(min=2, max=55)])
    ContactNo = StringField("Contact",
                             validators=[DataRequired(), Length(min=10, max=13)])
    DOB = StringField("DOB", validators=[DataRequired(), Length(min=2, max=55)])
    Street1 = StringField("Street Address Line 1", validators=[DataRequired()])
    Street2 = StringField("Street Address Line 2", validators=[DataRequired()])
    City = StringField("City", validators=[DataRequired()])
    State = StringField("State", validators=[DataRequired()])
    Zip = StringField("Zip Code", validators=[Length(min=6, max=6)])
    EmergencyContactName = StringField("Emergency contact Full Name", validators=[DataRequired()])
    EmergencyContactRelation = StringField("Emergency contact Relation", validators=[DataRequired()])
    EmergencyContactNumber = StringField("Emergency contact PhoneNo", validators=[DataRequired()])
    submit = SubmitField(" Update ")


class SearchPatient(FlaskForm):
    AadharNo = StringField("Aadhar",validators=[DataRequired()])
    submit = SubmitField("Go")


class RegistrationFormDoctor(FlaskForm):
    Email = StringField("Email", validators=[DataRequired(), Email()])
    Password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=15)])
    Password_confirm = PasswordField("Confirm Password",
                                     validators=[DataRequired(), Length(min=6, max=15), EqualTo('Password')])
    Name = StringField("Name", validators=[DataRequired(), Length(min=2, max=55)])
    Gender = StringField("Gender", validators=[DataRequired(), Length(min=2, max=55)])
    ContactNo = StringField("Contact",
                             validators=[DataRequired(), Length(min=10, max=13)])
    AadharNo = StringField("Aadhar", validators=[DataRequired(), Length(min=12, max=12)])
    CertificateNo= StringField("CertificateNo",validators=[DataRequired()])
    submit = SubmitField(" Register ")

    def validate_Email(self, Email):
        user = User.objects(Email=Email.data).first()
        if user:
            raise ValidationError("Email Exists")


class LoginFormDoctor(FlaskForm):
    Email = StringField("Email",validators=[DataRequired(), Email()])
    Password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=15)])
    submit = SubmitField("Login")



class RegistrationFormLab(FlaskForm):
    Email = StringField("Email", validators=[DataRequired(), Email()])
    Password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=15)])
    Password_confirm = PasswordField("Confirm Password",
                                     validators=[DataRequired(), Length(min=6, max=15), EqualTo('Password')])
    Name = StringField("Name", validators=[DataRequired(), Length(min=2, max=55)])
    ContactNo = StringField("Contact",
                             validators=[DataRequired(), Length(min=10, max=13)])
    AadharNo = StringField("Aadhar", validators=[DataRequired(), Length(min=12, max=12)])
    submit = SubmitField(" Register ")

class LoginFormLab(FlaskForm):
    Email = StringField("Email",validators=[DataRequired(), Email()])
    Password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=15)])
    submit = SubmitField("Login")