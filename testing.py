from app import app, db
from query.UserQuery import create_user, find_user_name, update_user
from model.models import User


user = create_user("Priyang", "2001-09-12", 'M', "9409481618", "123456789012")
print(user)

#find_user_name("UHP")
#update_user("123456789023", "9586244772")