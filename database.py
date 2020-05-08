import sqlite3
import hashlib
import datetime
import MySQLdb
from flask import session


def db_connect():
    _conn = MySQLdb.connect(host="localhost", user="root",
                            passwd="root", db="wine")
    c = _conn.cursor()

    return c, _conn

def user_reg(username,  email,password,  address,mobile):
    try:
        c, conn = db_connect()
        print(username,email, password,   address,mobile)
        j = c.execute("insert into user (username,  email,password,  address,mobile) values ('"+username +
                      "','"+email+"','"+password+"','"+address+"','"+mobile+"')")
        conn.commit()
        conn.close()
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))

def user_loginact(username, password):
    try:
        c, conn = db_connect()
        j = c.execute("select * from user where username='" +
                      username+"' and password='"+password+"'")
        c.fetchall()
        conn.close()
        return j
    except Exception as e:
        return(str(e))




if __name__ == "__main__":
    print(db_connect())