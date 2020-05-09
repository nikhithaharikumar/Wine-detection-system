import sqlite3
import hashlib
import datetime
import mysql.connector
from flask import session


def db_connect():
    _conn = mysql.connector.connect(host="localhost", user="root",
                            passwd="D!ngoo12", db="wine")
    c = _conn.cursor()

    return c, _conn

def user_reg(username,  email,password,  address,mobile):
    try:
        c, conn = db_connect()
        print(username,email, password,   address,mobile)
        insert_query = "insert into user (username,  email,password,  address,mobile) values ('"+username +\
                      "','"+email+"','"+password+"','"+address+"','"+mobile+"')"
        cursor = conn.cursor()
        cursor.execute(insert_query)
        records = cursor.fetchall()
        conn.commit()
        conn.close()
        print(records)
        return records
    except Exception as e:
        print(e)
        return(str(e))
    finally:
        if (conn.is_connected()):
            conn.close()
            cursor.close()
            print("MySQL connection is closed")

def user_loginact(username, password):
    try:
        c, conn = db_connect()
        select_query = "select * from user where username='" +\
                      username+"' and password='"+password+"'"
        cursor = conn.cursor()
        cursor.execute(select_query)
        records = cursor.fetchall()
        conn.close()
        return records
    except Exception as e:
        return(str(e))
    finally:
        if (conn.is_connected()):
            conn.close()
            cursor.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    print(db_connect())