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
    Gender = StringField("gender", validators=[DataRequired(), Length(min=2, max=55)])
    ContactNo = StringField("Contact",
                             validators=[DataRequired(), Length(min=10, max=13)])
    AadharNo = StringField("Aadhar", validators=[DataRequired(), Length(min=12, max=12)])
    DOB = StringField("DOB", validators=[DataRequired(), Length(min=2, max=55)])
    Street1 = StringField("Street Address Line 1")
    Street2 = StringField("Street Address Line 2")
    City = StringField("City")
    State = StringField("State")
    Zip = StringField("Zip Code", validators=[Length(min=6, max=6)])
    EmergencyContactName = StringField("Emergency contact Full Name")
    EmergencyContactRelation = StringField("Emergency contact Relation")
    EmergencyContactNumber = StringField("Emergency contact PhoneNo")
    submit = SubmitField("register")

    def validate_Email(self, Email):
        user = User.objects(Email=Email.data).first()
        if user:
            raise ValidationError("Email Exists")
