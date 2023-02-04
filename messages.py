from models import Message, User
from psycopg2 import connect, OperationalError
import argparse
import bcrypt


parser = argparse.ArgumentParser()

parser.add_argument('-u', '--username', help='username')
parser.add_argument('-p', '--password', help='password')
parser.add_argument('-t', '--to', help='message addressee')
parser.add_argument('-s', '--send', help='message')
parser.add_argument('-l', '--list', help='list messages to user', action='store_true')

args = parser.parse_args()


def list_messages(cursor, username, password):
    user = User.load_by_username(cursor, username)
    if not user:
        print('User does not exist')
    elif bcrypt.checkpw(bytes(password, encoding='utf-8'), user.hashed_password):
        messages = Message.load_all_messages(cursor)
        for message in messages:
            if message.to_id == user.id:
                print(message.date, ': ', message.mess)
    else:
        print('Password incorrect')