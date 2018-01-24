# Blubberduck: Pokémon Gogle

### Naotaka Kinoshita, Shakil Rafi, Michael Ruvinshteyn, Kelly Wang

[Watch our demo here](https://www.youtube.com/watch?v=bh83YKHzWWo)

Travel around the map to find Pokémon which you can catch and view in your Pokédex.

This uses the [Google Maps JavaScript API](https://developers.google.com/maps/documentation/javascript/) which provides a map for the user to travel around on as well as [PokeAPI](https://pokeapi.co/) which provides information about pokemon.

## Getting Started

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
5. Pokebase
   ```bash
   $ pip install pokebase --user
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
   $ git clone https://github.com/MRuvinshteyn/blubberduck.git
   $ cd blubberduck
   ```
5. Launch the app
   ```bash
   $ python app.py
   ```
6. Open a browser window and go to `http://localhost:5000`

That's it !!
