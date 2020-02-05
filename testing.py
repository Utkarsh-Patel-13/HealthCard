from query.UserQuery import create_user, find_user_name, update_user
from query.DoctorQuery import create_doctor
from app import app, db_user
from flask import request, render_template
from extrafuncs import check_aadhar_validity
from model.models import Address, Emergency
"""
add = Address("13 Prabhupark Society", "Radhanpur Road", "Mehsana", "Gujarat", "384002")
emer = Emergency("Utkarsh", "Patel", "9586244772")
user = create_user("Priyang", "2001-09-12", 'M', "9409481618", "123456789123", add, emer)
#user = create_doctor("Priyang", 'M', "9409481618", "123456789016", "111111")
print(user)

"""
find_user_name("UHP")
#update_user("123456789023", "9586244772")

"""
@app.route('/')
def index():
    return render_template('getAadhar.html')


@app.route('/', methods=["POST"])
def getvalue():
    aadharNo = request.form['aadhar']
    validity = check_aadhar_validity(aadharNo)
    user = db_user.find_one({'AadharNo': aadharNo})

    if validity == -1:
        txt = "Invalid Aadhar Number..."
        return render_template('getAadhar.html', msg=txt)
    elif user is not None:
        txt = "Aadhar already registered..."
        return render_template('getAadhar.html', msg=txt)
    else:
        return render_template('NewPatient.html', aadhar=aadharNo)


if __name__ == '__main__':
    app.run()
"""