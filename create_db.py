from psycopg2 import connect, OperationalError, DatabaseError


HOST = 'localhost'
USER = 'postgres'
PASSWORD = 'coderslab'

try:
    cnx = connect(host=HOST, user=USER, password=PASSWORD)
    cnx.autocommit = True
    sql = """CREATE DATABASE users;"""
    with cnx.cursor() as cursor:
        cursor.execute(sql)
except (OperationalError, DatabaseError) as err:
    if 'already exists' not in str(err):
        print('Unable to connect')
    print('database already exists')


