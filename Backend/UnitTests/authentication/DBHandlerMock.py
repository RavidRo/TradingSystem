"""this class is ment to be the gateway from the domain layer to the DB"""

from Backend.DataBase.Users import users


class DBHandlerMock(object):
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if DBHandlerMock.__instance is None:
            DBHandlerMock()
        return DBHandlerMock.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if DBHandlerMock.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DBHandlerMock.__instance = self
            self.users = {
                        'Tali':
                                {'password':'puppy',
                                'is_admin':'True'
                                 },
                        'Ravid':{'password':'dasi',
                                 'is_admin':'True'
                                 },
                        'Inon': {'password': 'guy',
                                'is_admin': ""
                                },
                        'Sean': {'password': 'Messi',
                                   'is_admin': ""
                                   },
                        'Omer': {'password': 'cool',
                                   'is_admin': ""
                                   }
            }

    def is_username_exists(self, username):
        return username in self.users

    def is_password_match(self, given_password, username):
        return self.users[username]['password'] == given_password

    def add_user_to_db(self, username, password):
        self.users[username] = {'password':password,'is_admin':""}

    def is_username_admin(self,username):
        return bool(self.users[username]['admin'])