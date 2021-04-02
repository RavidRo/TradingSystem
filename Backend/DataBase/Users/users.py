"""this class is a mockDB for users for now
    explanations:
    - all the passwords that are saved to the DB are hashed for security purposes
"""

from werkzeug.security import generate_password_hash, check_password_hash


class Users(object):
    """initializing the mockDB and inserting few users"""

    def __init__(self):
        self.users = dict()
        self.initialize_users_db()

    def initialize_users_db(self):
        self.add_user_to_db('tali', 'puppy',"")
        self.add_user_to_db('ravid', 'dasi',"True")
        self.add_user_to_db('sean', 'bunny',"")
        self.add_user_to_db('inon', 'guy',"")
        self.add_user_to_db('omer', 'cool',"")

    def is_username_exists(self, username):
        return username in self.users

    def is_password_match(self, given_password, username):
        return check_password_hash(self.users[username]['password'], given_password)

    """adds username and hashed password to DB"""

    def add_user_to_db(self, username, password, is_admin):
        self.users[username] = {
            'password':generate_password_hash(password, method='sha256'),
            'admin':is_admin
        }
