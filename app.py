import os, urllib2, json, random, pokebase
from flask import Flask, render_template, request, redirect, url_for, session, flash
from utils import db

app = Flask(__name__)
app.secret_key = os.urandom(32)

def logged_in():
    return 'user' in session

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

@app.route('/create',methods=['GET', 'POST'])
def create():
    if 'user' in session:
        return redirect('/')
    else:
        users = db.getUsers()
        print users
        print request.form.get('user')
        if request.form.get('user') in users:
            flash("u can't pick that name")
            return redirect(url_for('login'))
        if request.form.get('password') != request.form.get('confpass'):
            print "password"
            flash("Hey ur passwords are wrong")
            return redirect(url_for('login'))
        else:
            db.addUser(request.form.get('user'), request.form.get('password'))
            session['user'] = request.form.get('username')
            return redirect(url_for('map'))

@app.route('/auth',methods=['GET', 'POST'])
def auth():
    if 'user' in session:
        return redirect('/')
    else:
        users = db.getUsers()
        print users
        print request.form.get('user')
        if request.form.get('user') in users:
            print 'here:'
            print users[request.form.get('user')]
            if request.form.get('password') == users[request.form.get('user')]:
                session['user'] = request.form.get('user')
                return redirect(url_for('map'))
            else:
                flash ('thats not the right password')
                return redirect(url_for('login'))
        else:
            flash ('that person doesnt exist')
            return redirect(url_for('login'))

@app.route('/map')
def map():
    if 'user' in session:
        return render_template('map.html', title = 'Map', log = True)
    else:
        return redirect(url_for('root'))

@app.route('/profile')
def profile():
    if 'user' in session:
        pokemon = db.getPokemon('user')
        for key in pokemon:
            print key
            print pokemon[key]
        return render_template('profile.html', title = 'Profile', pokemon = pokemon )
    else:
        return redirect(url_for('auth'))
    
@app.route('/load_encounter')
def load_encounter():
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
    return redirect('/')

@app.route('/capture')
def capture():
    if 'user' in session:
        pokemon_id = session['encounter']
        pokemon_id = int(pokemon_id)
        pokemon = pokebase.pokemon(pokemon_id)
        db.addPokemon(session['user'], pokemon_id - 1, False)
        return render_template('capture.html',
                sprite = pokemon.sprites.front_default,
                name = pokemon.name,
                log = True)
    return redirect('/')

@app.route('/caught')
def caught():
    #player caught the pokemon in session['encounter']
    pokemon_id = session['encounter']
    pokemon_id = int(pokemon_id)
    db.addPokemon(session['user'], pokemon_id - 1, True)
    return redirect('/map')



if __name__ == '__main__':
    db.initDB()
    app.debug = True
    app.run()

