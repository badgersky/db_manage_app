from models import User
import argparse
from psycopg2 import errors
import bcrypt


UniqueViolation = errors.lookup('23505')


parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', help='username')
parser.add_argument('-p', '--password', help='min 8 characters')
parser.add_argument('-n', '--new_pass', help='new password')
parser.add_argument('-l', '--list', help='list users', action='store_true')
parser.add_argument('-d', '--delete', help='delete user')
parser.add_argument('-e', '--edit', help='edit user')

args = parser.parse_args()


def list_users(cur):
    users = User.load_all_users(cur)
    for user in users:
        print(user.username)


def create_user(username, password, cur):
    if len(password) < 8:
        print('Password is too short')
    else:
        new_user = User(username, password)
        try:
            new_user.save_to_db(cur)
        except UniqueViolation:
            print('User already exists')


def delete_user(username, password, cur):
    user = User.load_by_username(cur, username)
    if not user:
        print('User does not exist')
    elif bcrypt.checkpw(bytes(password, encoding='utf-8'), user.hashed_password):
        User.delete_user(cur, username)
    else:
        print('Incorrect password')


def edit_user(username, password, new_password, cur):
    user = User.load_by_username(cur, username)
    if not user:
        print('User does not exist')
    elif bcrypt.checkpw(bytes(password, encoding='utf-8'), user.hashed_password):
        if len(new_password) < 8:
            print('New password is too short')
        else:
            user.hashed_password = new_password
            user.save_to_db(cur)
    else:
        print('Incorrect password')










