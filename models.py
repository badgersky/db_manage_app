import bcrypt


class User:
    """class for managing user table in database"""

    def __init__(self, username, password=''):
        self._id = -1
        self.username = username
        self._hashed_password = bcrypt.hashpw(bytes(password), bcrypt.gensalt())

    @property
    def password(self):
        return self._hashed_password

    @property
    def id(self):
        return self._id

    @password.setter
    def password(self, new_password):
        self._hashed_password = bcrypt.hashpw(bytes(new_password), bcrypt.gensalt())
