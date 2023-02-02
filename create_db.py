from psycopg2 import connect, OperationalError, DatabaseError


HOST = 'localhost'
USER = 'postgres'
PASSWORD = 'coderslab'
DB = 'users_db'


def check_err(error):
    """checks what type of error occurs"""

    if 'already exists' in str(error):
        print('table/database already exists')
    else:
        print('unable to connect')


# database creation
cnx = connect(host=HOST, user=USER, password=PASSWORD)
cnx.autocommit = True
sql = """CREATE DATABASE users_db;"""
try:
    with cnx.cursor() as cursor:
        cursor.execute(sql)
except (OperationalError, DatabaseError) as err:
    check_err(err)
cnx.close()

# table users creation
cnx = connect(host=HOST, user=USER, password=PASSWORD, database=DB)
cnx.autocommit = True
users_sql = """CREATE TABLE users (id serial, username varchar(255) UNIQUE,
hashed_passw varchar(255), PRIMARY KEY (id));"""
try:
    with cnx.cursor() as cursor:
        cursor.execute(users_sql)
except (OperationalError, DatabaseError) as err:
    check_err(err)

# table messages creation
messages_sql = """CREATE TABLE messages (id serial, from_id int NOT NULL UNIQUE , to_id int NOT NULL UNIQUE,
message_date TIMESTAMP NOT NULL DEFAULT CURRENT_DATE, text varchar(255), PRIMARY KEY (id),
FOREIGN KEY (from_id) REFERENCES users(id) ON DELETE CASCADE,
FOREIGN KEY (TO_ID) REFERENCES users(id) ON DELETE CASCADE);"""
try:
    with cnx.cursor() as cursor:
        cursor.execute(messages_sql)
except (OperationalError, DatabaseError) as err:
    check_err(err)
cnx.close()
