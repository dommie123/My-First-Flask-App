#from werkzeug.security import safe_str_cmp # For Python 2.7 or below
from models.user_model import User

# These methods are used so that we don't have to iterate over the users list every time
# we want to add or search for a new user.
#username_mapping = {u.username: u for u in users}
#userid_mapping = {u.id: u for u in users}

# Retrieves a user by their username if they exist in the database and they typed the correct password.
def authenticate(username, password):
    user = User.find_by_username(username)
    if user and user.password == password:
        return user

# Retrieves a user by their id if they exist in the database.
def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)