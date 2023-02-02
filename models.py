import bcrypt
from psycopg2 import connect, OperationalError
from datetime import datetime


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
        else:
            sql_task = """UPDATE users SET username=%s, hashed_passw=%s WHERE id=%s;"""
            values = (self.username, self._hashed_password, self._id)
            cursor.execute(sql_task, values)

    @staticmethod
    def load_by_username(cursor, username):
        sql_task = """SELECT * FROM users WHERE username=%s;"""
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

    @staticmethod
    def load_by_id(cursor, user_id):
        sql_task = """SELECT * FROM users WHERE id=%s;"""
        cursor.execute(sql_task, (user_id,))
        data = cursor.fetchone()
        if not data:
            return None
        else:
            user_id, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = user_id
            loaded_user._hashed_password = hashed_password
            return loaded_user

    @staticmethod
    def load_all_users(cursor):
        sql_task = """SELECT * FROM users;"""
        cursor.execute(sql_task)
        data = cursor.fetchall()
        if not data:
            return None
        else:
            users = []
            for user in data:
                user_id, username, hashes_password = user
                loaded_user = User(username)
                loaded_user._id = user_id
                loaded_user._hashed_password = hashes_password
                users.append(loaded_user)
            return users

    @staticmethod
    def delete_user(cursor, username):
        sql_task = """DELETE FROM users WHERE username=%s;"""
        try:
            cursor.execute(sql_task, (username,))
        except OperationalError:
            print('error in delete_user')
        print('user deleted')
        return None


class Message:
    """class for managing messages in database"""

    def __init__(self, from_id, to_id, mess):
        self._id = -1
        self.date = None
        self.from_id = from_id
        self.to_id = to_id
        self.mess = mess

    @property
    def id(self):
        return self._id

    def save_to_db(self, cursor):
        if self._id == -1:
            sql_task = """INSERT INTO messages(from_id, to_id, message_date, text)VALUES(%s, %s, %s, %s) RETURNING id;"""
            self.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            values = (self.from_id, self.to_id, self.date, self.mess)
            cursor.execute(sql_task, values)
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql_task = """UPDATE messages SET from_id=%s, to_id=%s, message_date=$s, text=%s WHERE id=$s;"""
            values = (self.from_id, self.to_id, self.date, self.mess, self._id)
            cursor.execute(sql_task, values)
            return True

    @staticmethod
    def load_all_messages(cursor):
        sql_task = """SELECT * FROM messages;"""
        cursor.execute(sql_task)
        data = cursor.fetchall()
        if not data:
            return False
        else:
            messages = []
            for message in data:
                mess_id, from_id, to_id, date, text = message
                loaded_message = Message(from_id, to_id, text)
                loaded_message._id = mess_id
                loaded_message.date = date
                messages.append(loaded_message)
            return messages


if __name__ == '__main__':
    HOST = 'localhost'
    USER = 'postgres'
    PASSWORD = 'coderslab'
    DB = 'users_db'

    cnx = connect(host=HOST, user=USER, password=PASSWORD, database=DB)
    cnx.autocommit = True
    c = cnx.cursor()

    user4 = User('pancake', 'love_pancakes')
    user4.save_to_db(c)

    print(Message.load_all_messages(c))

    c.close()
    cnx.close()
