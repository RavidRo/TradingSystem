"""this class is a mockDB for users for now
    explanations:
    - all the passwords that are saved to the DB are hashed for security purposes
"""

from werkzeug.security import generate_password_hash, check_password_hash

class users(object):

    """initializing the mockDB and inserting few users"""
    def __init__(self):
        self.users = dict()
        self.initialize_users_db()

    def initialize_users_db(self):
        self.add_user_to_db('tali','puppy')
        self.add_user_to_db('ravid','dasi')
        self.add_user_to_db('sean','bunny')
        self.add_user_to_db('inon','guy')
        self.add_user_to_db('omer','cool')

    """returns a hash function of the given password"""
    def hash_password(self,password):
        return generate_password_hash(password, method='sha256')

    """gets a hashed password and the user's given password and checks wether
    the given password matches the DB hashed password"""
    def check_match(self,hashed_password,real_password):
        return  check_password_hash(hashed_password, real_password)

    """adds username and hashed password to DB"""
    def add_user_to_db(self,username,password):
        self.users[username] = self.hash_password(password=password)

    """checks if username is unique and if so, adds the user to the DB
    else generates an appropriate error message"""
    def register(self,username,password):
       if username in self.users:
           return "username already taken"
       else:
           self.add_user_to_db(username=username,password=password)
           return "succeeded"

    """checks if the user details match to those in the DB, if so returns a success message
    else, generates an appropriate error message"""
    def login(self,username,password):
       if username not in self.users:
           return "username doesn't exist"
       else:
           password_match = self.check_match(self.users[username], password)

           if password_match:
               return "succeeded"
           else:
               return "password incorrect"
