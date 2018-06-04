![Logo](https://raw.githubusercontent.com/house-ingetrac/la-finalissima/master/pokemonstay/static/img/pokemonstay_logo.png)


## Pokemon Stay 2: Electric Boogaloo
Alessandro Cartegni, Shakil Rafi, Samantha Ngo

Welcome to Pokemon Stay! This is Pokemon Go in Google Maps with battling and trading. We will be expanding on Team Blubber Duckies’ last term project by implementing battles, trades and an all expansive pokedex. Users will be able to see what pokemon they’ve caught, each pokemon’s stats, battle a Pokemon mastercomputer, and trade with other players!

[Droplet](http://206.189.231.92/)

This uses the [Google Maps JavaScript API](https://developers.google.com/maps/documentation/javascript/) which provides a map for the user to travel around on as well as [PokeAPI](https://pokeapi.co/) which provides information about pokemon.

## Want to Play Locally?

### Dependencies
1. Python 2.7
   ```bash
   $ sudo apt-get install python2.7
   ```
2. SQLite3
   ```bash
   $ sudo apt-get install sqlite3
   ```
3. Pip
   ```bash
   $ curl https://bootstrap.pypa.io/get-pip.py | sudo python 2.7
   ```
4. Flask
   ```bash
   $ pip install flask --user
   ```

### Setup

0. (Optional) Create and activate a virtual environment 
   ```bash
   $ virtualenv <name>
   $ . <name>/bin/activate
   ```
1. Install all dependencies listed above
2. Procure an API key for Google Maps from the following site: [GOOGLE MAPS API](https://developers.google.com/maps/documentation/javascript/)
   * Click "Get a key" and follow the given instructions
   * Insert your key into `GOOGLE_MAPS_API_KEY`
   * Example GOOGLE_MAPS_API_KEY file:
     ```
     EAKLN212asdf
     ```
3. Clone this repository
   ```bash
   $ git clone https://github.com/house-ingetrac/la-finalissima.git
   $ cd la-finalissima
   ```
5. Launch the app
   ```bash
   $ python app.py
   ```
6. Open a browser window and go to `http://localhost:5000`




<sub>This game is an extension of https://github.com/MRuvinshteyn/blubberduck.git</sub>
