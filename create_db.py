from psycopg2 import connect, OperationalError, DatabaseError


HOST = 'localhost'
USER = 'postgres'
PASSWORD = 'coderslab'
DB = 'users'


# database creation
cnx = connect(host=HOST, user=USER, password=PASSWORD)
cnx.autocommit = True
sql = """CREATE DATABASE users;"""
try:
    with cnx.cursor() as cursor:
        cursor.execute(sql)
except (OperationalError, DatabaseError) as err:
    print('database already exists')
cnx.close()


# table users creation
cnx = connect(host=HOST, user=USER, password=PASSWORD, database=DB)
cnx.autocommit = True
users_sql = """CREATE TABLE users (id serial, username varchar(255), hashed_passw varchar(80), PRIMARY KEY (id));"""
try:
    with cnx.cursor() as cursor:
        cursor.execute(users_sql)
except (OperationalError, DatabaseError) as err:
    if 'already exists' in str(err):
        print('table already exists')
