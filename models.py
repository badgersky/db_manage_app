import bcrypt
from psycopg2 import connect


class User:
    """class for managing user table in database"""

    def __init__(self, username, password=''):
        self._id = -1
        self.username = username
        self._hashed_password = bcrypt.hashpw(bytes(password, encoding='utf-8'), bcrypt.gensalt())

    @property
    def password(self):
        return self._hashed_password

    @property
    def id(self):
        return self._id

    @password.setter
    def password(self, new_password):
        self._hashed_password = bcrypt.hashpw(bytes(new_password, encoding='utf-8'), bcrypt.gensalt())

    def save_to_db(self, cursor):
        if self._id == -1:
            sql_task = """INSERT INTO users(username, hashed_passw) VALUES (%s, %s) RETURNING id;"""
            values = (self.username, self._hashed_password)
            cursor.execute(sql_task, values)
            self._id = cursor.fetchone()[0]
            return True
        return False

    @staticmethod
    def load_by_username(cursor, username):
        sql_task = """SELECT * FROM users WHERE username=%s"""
        cursor.execute(sql_task, (username,))
        data = cursor.fetchone()
        if not data:
            return None
        else:
            user_id, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = user_id
            loaded_user._hashed_password = hashed_password
            return loaded_user


if __name__ == '__main__':
    HOST = 'localhost'
    USER = 'postgres'
    PASSWORD = 'coderslab'
    DB = 'users_db'

    cnx = connect(host=HOST, user=USER, password=PASSWORD, database=DB)
    cnx.autocommit = True
    c = cnx.cursor()

    user2 = User('ottego', 'siemasie')
    user2.save_to_db(c)
    print(user2.id)
    print(User.load_by_username(c, 'amid4maru'))

    c.close()
    cnx.close()
