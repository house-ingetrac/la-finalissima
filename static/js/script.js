var map, heatmap, infoWindow, loc, dir, movement, lastLoc;
var mapDiv = document.getElementById('map');

var pkmnLocations = [];
var heatLocations = [];

var pkmn = [];

/***
 Loads pokemon from /load_encounter, which loads from pokebase. After 20 pokemon are
 added, waits until there is <20 pokemon loaded before getting new pokemon.
***/
function addpkmn(e) {
    if (e) {
        eval('pkmn.push(' + e + ');');
        console.log('loaded pokemon');
    }
    //dont load more than 20 pokemon
    if (pkmn.length > 20) {
        console.log('20 pokemon are already loaded');
        //wait 3 seconds before checking again
        setTimeout(addpkmn, 3000);
    } else {
        $.get('/load_encounter', addpkmn);
    }
}
addpkmn();

/***
 Main movement function that loops forever. Moves map on movement, checks for position
 updates to spawn new points on heatmap, checks if player has walked away from
 infoWindow and closes the window.
 ***/
function move() {
    //moving map around
    loc.lat = map.getCenter().lat();
    loc.lng = map.getCenter().lng();
    loc.lat += dir.lat;
    loc.lng += dir.lng;
    map.panTo(loc);

    encounter(); //checking if player has walked over heatmap

    //checking if player has walked away enough to spawn new heatmap points, if so, spawns
    if (google.maps.geometry.spherical.computeDistanceBetween(
        map.getCenter(), lastLoc) > 500) {
        lastLoc = map.getCenter();
        spawnHeatmaps();
    }

    //checking to see if player has walked away from an open infoWindow and closes it
    if (infoWindow != null && google.maps.geometry.spherical.computeDistanceBetween(
        map.getCenter(), infoWindow.position) > 100) {
        infoWindow.close();
        infoWindow = null;
    }
}

/***
 Movement functions, on keyDown changes player sprite to running sprite
 ***/
function keyDownHandler(e) {
    switch (e.keyCode) {
        case 37:
            document.head.appendChild(document.createElement("style")).innerHTML = "#map:after {background-image: url('/static/img/run.gif');}";
            dir.lng = -0.00005;
            break;
        case 38:
            document.head.appendChild(document.createElement("style")).innerHTML = "#map:after {background-image: url('/static/img/run.gif');}";
            dir.lat = 0.00005;
            break;
        case 39:
            document.head.appendChild(document.createElement("style")).innerHTML = "#map:after {background-image: url('/static/img/run.gif');}";
            dir.lng = 0.00005;
            break;
        case 40:
            document.head.appendChild(document.createElement("style")).innerHTML = "#map:after {background-image: url('/static/img/run.gif');}";
            dir.lat = -0.00005;
            break;
    }
}

/***
 Movement functions, on keyUp changes player sprite back to stopped sprite
 ***/
function keyUpHandler(e) {
    switch (e.keyCode) {
        case 37:
            document.head.appendChild(document.createElement("style")).innerHTML = "#map:after {background-image: url('/static/img/player_sprite.png');}";
            dir.lng = 0;
            break;
        case 38:
            document.head.appendChild(document.createElement("style")).innerHTML = "#map:after {background-image: url('/static/img/player_sprite.png');}";
            dir.lat = 0;
            break;
        case 39:
            document.head.appendChild(document.createElement("style")).innerHTML = "#map:after {background-image: url('/static/img/player_sprite.png');}";
            dir.lng = 0;
            break;
        case 40:
            document.head.appendChild(document.createElement("style")).innerHTML = "#map:after {background-image: url('/static/img/player_sprite.png');}";
            dir.lat = 0;
            break;
    }
}

/***
 Initializes map centered on Times Square, disables standard map controls, sets up
 base heatmap, and gets ready for plater to move around with arrow keys.
 ***/
function initMap() {
    loc = {lat: 40.758896, lng: -73.985130}; //times square
    dir = {lat: 0, lng: 0};

    //initializing map with controls, etc.
    map = new google.maps.Map(mapDiv, {
        zoom: 17,
        center: loc,
        mapTypeId: 'roadmap',
        gestureHandling: 'none',
        keyboardShortcuts: false,
        zoomControl: false,
        disableDefaultUI: true
    });

    //initializing array for heatmap and heatmap
    pkmnLocations = new google.maps.MVCArray(heatLocations);
    heatmap = new google.maps.visualization.HeatmapLayer({
        data: pkmnLocations,
        map: map,
        radius: 70
    });
    heatmap.setMap(map);

    //listening for arrow keys for movement
    window.addEventListener('keydown', keyDownHandler);
    window.addEventListener('keyup', keyUpHandler);

    lastLoc = map.getCenter(); //setting location to track when to spawn points
    movement = setInterval(move, 25); //looping function
}

/***
 Spawns a random number of heatmap points as player moves around in a random
 direction/radius around the player.
 ***/
function spawnHeatmaps() {
    //choosing random number of points
    var numPoints = Math.floor(Math.random() * 10);
    console.log("spawn");

    //adding points
    for (var i = 0; i < numPoints; i ++) {

        //choosing random distance from player and heading
        var randDist = Math.random() * (.005 - .0005) + .0005;
        var xHeading = Math.random();
        var yHeading = Math.random();
        if (xHeading < .5) xHeading = -1;
        else xHeading = 1;
        if (yHeading < .5) yHeading = -1;
        else yHeading = 1;

        //adding point
        console.log("xHead " + xHeading + " yHead " + yHeading + " randDist " + randDist);
        var point = new google.maps.LatLng(map.getCenter().lat() +(xHeading * randDist),
            map.getCenter().lng() + (yHeading * randDist));
        pkmnLocations.push(point);
    }
}

/***
 Tests to see if the player is "close enough" to the heatmap/location of a Pokemon.
 If player is close enough, then the location of the pokemon is returned, and a Pokemon
 can no longer spawn in that location.
 If not, -1 is returned.
 ***/
function closeEnough(){
    //looping through all heatmap points to see if player is close to one
    for (var i = 0; i < pkmnLocations.getLength(); i ++) {
        if (google.maps.geometry.spherical.computeDistanceBetween(
            map.getCenter(), pkmnLocations.getAt(i)) < 50) {
            //remove and return location if player is close enough
            var loc = pkmnLocations.getAt(i);
            pkmnLocations.removeAt(i);
            return loc;
        }
    }
    return -1; //not closeEnough
}

/***
 Spawns InfoWindow objects at locations of Pokemon.
 Calls closeEnough() to see if the player is close to a heatmap/Pokemon location, if
 closeEnough() returns a location, then there is a chance of the InfoWindow spawning.
 The InfoWindow contains an image of the Pokemon encountered as well as name of pokemon
 and a link to capture the Pokemon.
 ***/
function encounter() {
    var dist = closeEnough(); //check to see if player is closeEnough to any pkmn
    if (dist != -1) {

        //set content of infoWindow with sprite, pkmn name
        var spawn = pkmn.pop(); //pop pokemon from list of loaded pokemon
        var contentString, sprite;
        if (spawn && Math.random() < .5) { //if there are pokemon and within %chance
            contentString = "You found:<br>" + spawn.name[0].toUpperCase() +
                            spawn.name.substr(1); //capitalize pokemon name
            sprite = spawn.sprite;
        } else { //no pokemon
            contentString = "Just grass";
            sprite = "/static/img/grass.png";
        }
        if (infoWindow) { //if there is already an infoWindow open
            infoWindow.close();
        }
        infoWindow = new google.maps.InfoWindow({
            content:
            "<div style='float:left'>" +
            "<img src='" + sprite + "' width='100px'></div>" +
            "<div style='float:right; padding: 10px;'>" +
            "<h4>" + contentString + "</h4></div>"
        });
        infoWindow.setPosition(dist); //set position of infoWindow on heatmap point
        infoWindow.open(map); //display infoWindow
    }
}
