from models import Message, User
from psycopg2 import connect, OperationalError
import argparse
from passw_hash import check_password


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
    elif check_password(password, user.password):
        messages = Message.load_all_messages(cursor)
        for message in messages:
            if message.to_id == user.id:
                print(f'addressee: {user.username}')
                print(f'date: {message.date}')
                print(f'text: {message.mess}')
    else:
        print('Password incorrect')


def send_message(cursor, username, password, addressee, message):
    user = User.load_by_username(cursor, username)
    if not user:
        print('User does not exist')
    elif check_password(password, user.password):
        user_to = User.load_by_username(cursor, addressee)
        if not user_to:
            print('Pointed addressee does not exist')
        else:
            if len(message) > 255:
                print('Message is to long')
            else:
                m = Message(user.id, user_to.id, message)
                m.save_to_db(cursor)
    else:
        print('Password is incorrect')


if __name__ == '__main__':
    HOST = 'localhost'
    USER = 'postgres'
    PASSWORD = 'coderslab'
    DB = 'users_db'

    try:
        cnx = connect(host=HOST, user=USER, password=PASSWORD, database=DB)
        cnx.autocommit = True
        c = cnx.cursor()

        if args.username and args.password and args.list:
            list_messages(c, args.username, args.password)
        elif args.username and args.password and args.to and args.send:
            send_message(c, args.username, args.password, args.to, args.send)

        c.close()
        cnx.close()

    except OperationalError as e:
        print('error: ', e)
