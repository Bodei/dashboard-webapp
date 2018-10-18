import psycopg2 as p

DATABASE_URL = 'postgres://rnbdhoioobthuw:80e11f84e08dc2bba946755b2948eafa8cf65ad135c89b5c906ef5b46eeb4e8a@ec2-184-72-234-230.compute-1.amazonaws.com:5432/d10ej7g8l0em9b'
import urllib.parse as urlparse
import os

url = urlparse.urlparse(DATABASE_URL)
dbname = url.path[1:]
user = url.username
password =url.password
host = url.hostname
port = url.port

def connect_db():
    try:
        con = p.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port)

        cur = con.cursor() # as list
    except:
        print('No connection with Heroku database! DB is local and NO live data streaming!')
        con = p.connect(dbname='testdata_local', user='royfitz', password='password', host='localhost')
        cur = con.cursor() # as list

    try:
        cur.execute("CREATE TABLE testdata ("
                    "id serial PRIMARY KEY, "
                    "date_time timestamtz,"
                    "duration interval,"
                    "temperature integer,"
                    "humidity integer);")
        con.commit()
        print('Database table for test results created!')
    except:
        print('Database table for results already exists! Data will be cleared!')
        cur.execute('rollback;')

    #create a table to parse test relevant inputs to  heroku app
    try:
        cur.execute("CREATE TABLE testinputs (start timestamptz, rec_interval integer, "
                    "mt float, bt float,mh float, bh float);")
        con.commit()
        print('Database table for test inputs created!')
    except:
        print('Database table for inputs already exists! Data will be cleared!')
        cur.execute('rollback;')

    return con, cur

