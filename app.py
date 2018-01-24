import os, urllib2, json, random, pokebase
from flask import Flask, render_template, request, redirect, url_for, session, flash
from utils import db

app = Flask(__name__)
app.secret_key = os.urandom(32)

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
    with open('GOOGLE_MAPS_API_KEY', 'rU') as key_file:
        key = key_file.read().strip()
    script = urllib2.urlopen('https://maps.googleapis.com/maps/api/js?key=%s&libraries=visualization,geometry&callback=initMap' % key)
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
        users = db.getUsers()
        if request.form.get('user') in users: #username already exists
            flash("u can't pick that name")
            return redirect(url_for('login'))
        if request.form.get('password') != request.form.get('confpass'): #passwords dont match
            # print "password"
            flash("Hey ur passwords are wrong")
            return redirect(url_for('login'))
        else:
            #success! log in and view the map
            db.addUser(request.form.get('user'), request.form.get('password'))
            session['user'] = request.form.get('user')
            # print "Made account for %s" % request.form.get('user')
            return redirect(url_for('map'))

@app.route('/auth',methods=['GET', 'POST'])
def auth():
    if 'user' in session:
        return redirect('/')
    else:
        users = db.getUsers()
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
        raw_pokemon = db.getPokemon(session['user'])
        pokemon = []
        #list of all the pokemon you've encountered and info about them
        for key in raw_pokemon:
            pokedata = pokebase.pokemon( int(key)+1)
            this_pokemon = {}
            this_pokemon['sprite'] = pokedata.sprites.front_default.encode('ascii', 'ignore')
            this_pokemon['id'] = pokedata.id
            this_pokemon['name'] = pokedata.name.encode('ascii', 'ignore').title()
            this_pokemon['type1'] = pokedata.types[0].type.name.title()
            if len(pokedata.types) > 1:
                #type1: this pokemon has been caught!
                #type2: encountered but not caught
                this_pokemon['type2'] = pokedata.types[1].type.name.title()
            else:
                this_pokemon['type2'] = ''
            if raw_pokemon[key] == '1':
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
    pokemon_choice = db.getPokemonWithRarity(rarity)
    pokemon = pokebase.pokemon(pokemon_choice[0])
    pokedict = {}
    pokedict['name'] = pokemon.name.encode('ascii', 'ignore')
    pokedict['sprite'] = pokemon.sprites.front_default.encode('ascii', 'ignore')
    pokedict['id'] = pokemon.id
    return pokedict.__str__()

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
        pokemon = pokebase.pokemon(pokemon_id)
        db.addPokemon(session['user'], pokemon_id - 1, False) #false- pokemon has been encountered, not caught
        return render_template('capture.html',
                sprite = pokemon.sprites.front_default,
                name = pokemon.name,
                title = pokemon.name,
                log = True)
    return redirect('/')

#update pokemon blob from users table
@app.route('/caught')
def caught():
    #player caught the pokemon in session['encounter']
    pokemon_id = session['encounter']
    pokemon_id = int(pokemon_id)
    db.addPokemon(session['user'], pokemon_id - 1, True)
    #success! go back to the map
    return redirect('/map')


if __name__ == '__main__':
    db.initDB()
    app.debug = True
    app.run()

