import sqlite3, os, csv
from flask import request, flash

def initDB():
    if not os.path.exists('data/databases.db'):
        print "Creating database..."
        db = sqlite3.connect("data/databases.db")
        c = db.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS users (user TEXT, pass TEXT, pokemon TEXT, PRIMARY KEY(user))")
        c.execute("CREATE TABLE IF NOT EXISTS pokemon_by_rarity (id INT, name TEXT, rarity INT)")
        with open("data/pokemon_rarity.csv", "rU") as rarity_csv_file:
            next(rarity_csv_file)
            csvreader = csv.reader(rarity_csv_file)
            for row in csvreader:
                print "INSERT INTO pokemon_by_rarity VALUES(%s,'%s',%s)" % (row[0], row[1], row[2])
                c.execute("INSERT INTO pokemon_by_rarity VALUES(%s,\"%s\",%s)" % (row[0], row[1], row[2]))
        db.commit()
        db.close()
        print "Created database"

#add username and password to database
def addUser(user, pazz ):
    db = sqlite3.connect("data/databases.db")
    c = db.cursor()
    c.execute("INSERT INTO users VALUES(?,?,?)", (user,pazz,'0'*721))
    db.commit()
    db.close()

def addPokemon( user, pokemon , captured):
    db = sqlite3.connect("data/databases.db")
    c = db.cursor()
    c.execute("SELECT pokemon from users where users.user = '%s'" % user)
    oldBlob = c.fetchone()[0].encode('ascii', 'ignore')
    if captured:
        oldBlob = oldBlob[:pokemon] + '2' + oldBlob[pokemon + 1:]
    elif oldBlob[pokemon] != '2':
        oldBlob = oldBlob[:pokemon] + '1' + oldBlob[pokemon + 1:]
    execute_this = "UPDATE users SET pokemon = '%s' WHERE users.user = '%s'" % (oldBlob, user)
    c.execute(execute_this)
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

def getPokemon(usern):
    db = sqlite3.connect("data/databases.db")
    c = db.cursor()
    a = 'SELECT pokemon FROM users WHERE users.user ="'+ usern + '"'
    x = c.execute(a)
    pokemon = { }
    for key in x:
        for ke in key:
            for i in range(0,721):
                num = ke.encode('ascii','ignore')[i]
                print num
                if num == '2':
                    if 'caught' not in pokemon:
                        pokemon['caught'] = i+1
                    else:
                        pokemon['caught'].append(i+1)
                    print "added caught!"
                if num == '1':
                    if 'encountered' not in pokemon:
                        pokemon['encountered'] = i+1
                    else:
                        pokemon['encountered'].append(i+1)
                    print "added encountered!"
    db.close()
    return pokemon

def findPokemon(num):
    url = "http://pokeapi.co/api/v2/pokemon/" + num + "/"

def getPokemonWithRarity(rarity):
    db = sqlite3.connect("data/databases.db")
    c = db.cursor()
    pokemon_list = c.execute("SELECT id FROM pokemon_by_rarity WHERE rarity = %d ORDER BY RANDOM() LIMIT 1" % rarity)
    return pokemon_list.fetchone()

'''
x = getPokemon('kelly')
for key in x:
    print key
    print x[key]

'''
