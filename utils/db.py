import sqlite3
from flask import request, flash

db = sqlite3.connect("data/databases.db")
c = db.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users (user TEXT, pass TEXT, PRIMARY KEY(user))")
db.commit()
db.close()

#add username and password to database
def addUser(user, pazz ):
    db = sqlite3.connect("data/databases.db")
    c = db.cursor()
    c.execute("INSERT INTO users VALUES(?,?)", (user,pazz))
    db.commit()
    db.close()

def getUsers():
    db = sqlite3.connect("data/databases.db")
    c = db.cursor()
    a = 'SELECT user, pass FROM users'
    x = c.execute(a)
    users = {}
    for line in x:
        users[line[0]] = line[1]
    db.close()
    return users
