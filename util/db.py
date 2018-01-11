import sqlite3
from flask import request, flash

if __name__ == '__main__':
    db = sqlite3.connect("data/databases.db")
    c = db.cursor()
    c.execute("CREATE TABLE users (user TEXT, pass TEXT, PRIMARY KEY(user))")
    db.commit()
    db.close()

#add username and password to database
def addUser(user, pazz ):
    db = sqlite3.connect("data/databases.db")
    c = db.cursor()
    c.execute("INSERT INTO users VALUES(?,?)", (user,pazz))
    db.commit()
    db.close()

