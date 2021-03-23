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
        self.add_user_to_db('tali', 'puppy', 1)
        self.add_user_to_db('ravid', 'dasi', 2)
        self.add_user_to_db('sean', 'bunny', 3)
        self.add_user_to_db('inon', 'guy', 4)
        self.add_user_to_db('omer', 'cool', 5)

    def is_username_exists(self, username):
        return username in self.users

    def is_password_match(self, given_password, username):
        return check_password_hash(self.users[username]["password"], given_password)

    """adds username and hashed password to DB"""

    def add_user_to_db(self, username, password, cookie):
        self.users[username] = {
            "password": generate_password_hash(password, method='sha256'),
            "cookie": cookie
        }

    def get_cookie(self, username):
        return self.users[username]["cookie"]
