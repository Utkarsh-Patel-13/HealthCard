from query.UserQuery import create_user, find_user_name, update_user
from query.DoctorQuery import create_doctor


#user = create_user("Priyang", "2001-09-12", 'M', "9409481618", "123456789015")
user = create_doctor("Priyang", 'M', "9409481618", "123456789015", "111112")
print(user)

#find_user_name("UHP")
#update_user("123456789023", "9586244772")