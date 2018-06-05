from __init__ import dbase
import os, csv

base_dir = os.path.abspath(os.path.dirname(__file__))

class User(dbase.Model):
    id = dbase.Column(dbase.Integer, primary_key = True)
    username = dbase.Column(dbase.String(80), unique = True)
    password = dbase.Column(dbase.String(80))
    display_name = dbase.Column(dbase.String(80))
    pokemon_list = dbase.Column(dbase.String(721))

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.display_name = ''
        self.pokemon_list = '0'*721

    def __repr__(self):
        return '<User %r>' % self.username

class Pokemon(dbase.Model):
    id = dbase.Column(dbase.Integer, primary_key = True)
    name = dbase.Column(dbase.String(30))
    rarity = dbase.Column(dbase.Integer)
    ability_id = dbase.Column(dbase.Integer)
    type_id_1 = dbase.Column(dbase.Integer)
    type_id_2 = dbase.Column(dbase.Integer)
    weight = dbase.Column(dbase.Integer)
    height = dbase.Column(dbase.Integer)
    hp = dbase.Column(dbase.Integer)
    attack = dbase.Column(dbase.Integer)
    defense = dbase.Column(dbase.Integer)
    sp_attack = dbase.Column(dbase.Integer)
    sp_defense = dbase.Column(dbase.Integer)
    speed = dbase.Column(dbase.Integer)
    description = dbase.Column(dbase.String(500))

    def __init__(self, id, name, rarity, ability_id, type_id_1, type_id_2, weight, height, hp, attack, defense, sp_attack, sp_defense, speed, description):
        self.id = id
        self.name = name
        self.rarity = rarity
        self.ability_id = ability_id
        self.type_id_1 = type_id_1
        self.type_id_2 = type_id_2
        self.weight = weight
        self.height = height
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.sp_attack = sp_attack
        self.sp_defense = sp_defense
        self.speed = speed
        self.description = description

    def __repr__(self):
        return '<Pokemon %s>' % self.name

class Type(dbase.Model):
    id = dbase.Column(dbase.Integer, primary_key = True)
    name = dbase.Column(dbase.String(30))

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<Type %s>' % self.name

class Ability(dbase.Model):
    id = dbase.Column(dbase.Integer, primary_key = True)
    name = dbase.Column(dbase.String(30))
    description = dbase.Column(dbase.String(200))

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Ability %s>' % self.name

def init_db():
    if not Pokemon.query.filter_by(id = 1).first():
        with open(base_dir + "/data/pokemon_compiled_data.csv", "rU") as compiled_csv_data:
            next(compiled_csv_data)
            csvreader = csv.reader(compiled_csv_data)
            for row in csvreader:
                pokemon = Pokemon(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14])
                dbase.session.add(pokemon)
                dbase.session.commit()
