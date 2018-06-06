import os, urllib2, json, random, pokebase, csv
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from utils import db

app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'shhh issa secret'
app.secret_key = 'shhh issa secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'data/app_test.db')
dbase = SQLAlchemy(app)
from models import *
dbase.create_all()

def logged_in():
    return 'user' in session

#root route
@app.route('/')
def root():
    if 'user' in session:
        return redirect('/map')
    else:
        return render_template('home.html', title = 'Home', log = False)

@app.route('/map_script')
def map_script():
    key = ''
    with open(base_dir + '/GOOGLE_MAPS_API_KEY', 'rU') as key_file:
        key = key_file.read().strip()
    url = 'https://maps.googleapis.com/maps/api/js?key=%s&libraries=visualization,geometry&callback=initMap' % key
    print 'key = ', key
    print 'url = ', url
    script = urllib2.urlopen(url)
    return script.read()

@app.route('/login',methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect('/')
    else:
        return render_template('login.html', title = 'Login', log = False)

@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect('/')

#create an account
@app.route('/create',methods=['GET', 'POST'])
def create():
    if 'user' in session:
        return redirect('/')
    else:
        users_result = User.query.all()
        users = {}
        for line in users_result:
            users[line.username] = line.password
        if request.form.get('user') in users: #username already exists
            flash("u can't pick that name")
            return redirect(url_for('login'))
        if request.form.get('password') != request.form.get('confpass'): #passwords dont match
            # print "password"
            flash("Hey ur passwords are wrong")
            return redirect(url_for('login'))
        else:
            #success! log in and view the map
            uname = request.form.get('user')
            pword = request.form.get('password')
            dbase.session.add(User(uname, pword))
            dbase.session.commit()
            session['user'] = request.form.get('user')
            # print "Made account for %s" % request.form.get('user')
            return redirect(url_for('map'))

@app.route('/auth',methods=['GET', 'POST'])
def auth():
    if 'user' in session:
        return redirect('/')
    else:
        users_result = User.query.all()
        users = {}
        for line in users_result:
            users[line.username] = line.password
        if request.form.get('user') in users:
            #success! log in and view the map
            if request.form.get('password') == users[request.form.get('user')]:
                session['user'] = request.form.get('user')
                return redirect(url_for('map'))
            #can not log in :(
            else:
                flash ('thats not the right password')
                return redirect(url_for('login'))
        else:
            flash ('that person doesnt exist')
            return redirect(url_for('login'))

#view the map
@app.route('/map')
def map():
    if 'user' in session:
        return render_template('map.html', title = 'Map', log = True)
    else:
        return redirect(url_for('root'))

@app.route('/profile')
def profile():
    if 'user' in session:
        raw_pokemon = User.query.filter_by(username = session['user']).first().pokemon_list
        pokemon = []
        #list of all the pokemon you've encountered and info about them
        for id, val in enumerate(raw_pokemon):
            if val == '0':
                continue
            pokedata = Pokemon.query.filter_by(id=(int(id))).first()
            this_pokemon = {}
            this_pokemon['sprite'] = get_sprite(pokedata.id)
            this_pokemon['id'] = pokedata.id
            this_pokemon['name'] = pokedata.name
            this_pokemon['type1'] = pokedata.type_id_1
            this_pokemon['type2'] = pokedata.type_id_2
            if val == '1':
                this_pokemon['caught'] = False
            else:
                this_pokemon['caught'] = True
            pokemon.append(this_pokemon)
        return render_template('profile.html', 
                title = 'Profile', 
                pokemon = pokemon,
                log = True)
    else:
        return redirect('/login')
    
@app.route('/load_encounter')
def load_encounter():
    #spawn pokemon based on rarity
    rarity_list = [1]*10 + [2]*9 + [3]*8 + [4]*7 + [5]*6 + [6]*5 + [7]*4 + [8]*3 + [9]*2 + [10]
    rarity = random.choice(rarity_list)
    pokemon_choice = random.choice(Pokemon.query.filter_by(rarity=rarity).all())
    pokedict = {}
    pokedict['name'] = pokemon_choice.name.encode('ascii')
    pokedict['sprite'] = get_sprite(pokemon_choice.id)
    pokedict['id'] = pokemon_choice.id
    return pokedict.__str__()

def get_sprite(pokemon_id):
    return 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/%d.png' % pokemon_id

@app.route('/set_capture/<int:pokemon_id>')
def set_capture(pokemon_id):
    session['encounter'] = pokemon_id
    return ''

#encounter a pokemon
@app.route('/capture')
def capture():
    if 'user' in session:
        pokemon_id = session['encounter']
        pokemon_id = int(pokemon_id)
        u = User.query.filter_by(username = session['user']).first()
        old_blob = u.pokemon_list
        old_blob = old_blob[:pokemon_id] + '1' + old_blob[pokemon_id + 1:]
        u.pokemon_list = old_blob
        dbase.session.add(u)
        dbase.session.commit()
        pokemon = Pokemon.query.filter_by(id=pokemon_id).first()
        return render_template('capture.html',
                sprite = get_sprite(pokemon.id),
                name = pokemon.name,
                title = pokemon.name,
                log = True)
    return redirect('/')

#update pokemon column from users table
@app.route('/caught')
def caught():
    #player caught the pokemon in session['encounter']
    pokemon_id = session['encounter']
    pokemon_id = int(pokemon_id)
    u = User.query.filter_by(username = session['user']).first()
    old_blob = u.pokemon_list
    old_blob = old_blob[:pokemon_id] + '2' + old_blob[pokemon_id + 1:]
    u.pokemon_list = old_blob
    dbase.session.add(u)
    dbase.session.commit()
    #success! go back to the map
    return redirect('/map')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
