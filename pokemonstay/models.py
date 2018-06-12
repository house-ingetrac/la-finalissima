from __init__ import db
import os, csv

base_dir = os.path.abspath(os.path.dirname(__file__))

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True)
    password = db.Column(db.String(80))
    display_name = db.Column(db.String(80))
    pokemon_list = db.Column(db.String(721))

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.display_name = ''
        self.pokemon_list = '0'*721

    def __repr__(self):
        return '<User %r>' % self.username

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    rarity = db.Column(db.Integer)
    ability_id = db.Column(db.Integer)
    type_id_1 = db.Column(db.Integer)
    type_1 = db.Column(db.String(20))
    type_id_2 = db.Column(db.Integer)
    type_2 = db.Column(db.String(20))
    weight = db.Column(db.Integer)
    height = db.Column(db.Integer)
    hp = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    sp_attack = db.Column(db.Integer)
    sp_defense = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    description = db.Column(db.String(500))

    def __init__(self, id, name, rarity, ability_id, type_id_1, type_1, type_id_2, type_2, weight, height, hp, attack, defense, sp_attack, sp_defense, speed, description):
        self.id = id
        self.name = name
        self.rarity = rarity
        self.ability_id = ability_id
        self.type_id_1 = type_id_1
        self.type_1 = type_1
        self.type_id_2 = type_id_2
        self.type_2 = type_2
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

class Type(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<Type %s>' % self.name

class Ability(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(200))

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Ability %s>' % self.name

def init_db():
    if not Pokemon.query.filter_by(id = 1).first():
        with open(base_dir + "/data/types.csv", "rU") as type_csv_data:
            next(type_csv_data)
            csvreader = csv.reader(type_csv_data)
            for row in csvreader:
                t = Type(row[0], row[1])
                db.session.add(t)
            db.session.commit()

        with open(base_dir + "/data/pokemon_compiled_data.csv", "rU") as compiled_csv_data:
            next(compiled_csv_data)
            csvreader = csv.reader(compiled_csv_data)
            for row in csvreader:
                type_1 = Type.query.filter_by(id = row[4]).first().name
                type_2 = Type.query.filter_by(id = row[5]).first().name
                pokemon = Pokemon(row[0], row[1], row[2], row[3], row[4], type_1, row[5], type_2, row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14])
                db.session.add(pokemon)
            db.session.commit()
