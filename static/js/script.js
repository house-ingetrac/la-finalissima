var map, heatmap, infoWindow, loc, dir, movement, heatPoints;
var mapDiv = document.getElementById('map');

var pkmnLocations = [];
var heatLocations = [];

function move() {
  //console.log('moving');
  loc.lat = map.getCenter().lat();
  loc.lng = map.getCenter().lng();
  loc.lat += dir.lat;
  loc.lng += dir.lng;
  //console.log(loc);
  map.panTo(loc);
  encounter();
}

function keyDownHandler(e) {
    //console.log('keydown');
    switch (e.keyCode) {
        case 37:
            dir.lng = -0.00005;
            break;
        case 38:
            dir.lat = 0.00005;
            break;
        case 39:
            dir.lng = 0.00005;
            break;
        case 40:
            dir.lat = -0.00005;
            break;
    }
}

function keyUpHandler(e) {
    //console.log('keyup');
    switch (e.keyCode) {
        case 37:
            dir.lng = 0;
            break;
        case 38:
            dir.lat = 0;
            break;
        case 39:
            dir.lng = 0;
            break;
        case 40:
            dir.lat = 0;
            break;
    }
}

/***
 Initializes map centered on Times Square, disables standard map controls, sets up
 base heatmap, and gets ready for plater to move around with arrow keys.
***/
function initMap() {
  loc = {lat: 40.758896, lng: -73.985130};
  dir = {lat: 0, lng: 0};
  map = new google.maps.Map(mapDiv, {
    zoom: 17,
    center: loc,
    mapTypeId: 'roadmap',
    gestureHandling: 'none',
    keyboardShortcuts: false,
    zoomControl: false,
    disableDefaultUI: true
  });
  pkmnLocations = new google.maps.MVCArray(heatLocations);
  heatmap = new google.maps.visualization.HeatmapLayer({
    data: pkmnLocations,
    map: map,
    radius: 70
  });
  heatmap.setMap(map);
  window.addEventListener('keydown', keyDownHandler);
  window.addEventListener('keyup', keyUpHandler);
  movement = setInterval(move, 25);
}


/***
 Generates random points based on a specific lat/long combination to add randomness
 to the heatmap.
***/
function genRandPoints(numPoints, lat, long) {
  var ret = [];
  var randLat;
  var randLong;
  var location = new google.maps.LatLng(lat, long);
  pkmnLocations.push(location);
  for (var i = 0; i < numPoints; i ++) {
    randLat = Math.random() * 0.001;
    randLong = Math.random() * 0.001;
    ret.push(new google.maps.LatLng(lat + randLat, long + randLong));
  }
  console.log(ret);
  return ret;
}

function getPoints() {
    return genRandPoints(20, 40.76, -73.99);
    //new google.maps.LatLng(37.751266, -122.403355)
}

function heater() {
  /***
  var points = getPoints();
  for (var i = 0; i < points.length; i ++) {
    heatPoints.push(points[i]);
  }
   ***/
  var point = new google.maps.LatLng(40.76, -73.99);
  //heatPoints.push(point);
  pkmnLocations.push(point);
}

/***
 Tests to see if the player is "close enough" to the heatmap/location of a Pokemon.
 If player is close enough, then the location of the pokemon is returned, and a Pokemon
 can no longer spawn in that location.
 If not, -1 is returned.
***/
function closeEnough() {
  for (var i = 0; i < pkmnLocations.getLength(); i ++) {
    if (google.maps.geometry.spherical.computeDistanceBetween(map.getCenter(),
                                                              pkmnLocations.getAt(i)) < 50) {
      var loc = pkmnLocations.getAt(i);
      pkmnLocations.removeAt(i);
      return loc;
    }
  }
  return -1;
}

/***
 Spawns InfoWindow objects at locations of Pokemon.
 Calls closeEnough() to see if the player is close to a heatmap/Pokemon location, if
 closeEnough() returns a location, then there is a chance of the InfoWindow spawning.
 The InfoWindow contains an image of the Pokemon encountered as well as a brief
 description, and a link to capture the Pokemon.
***/
function encounter() {
  //console.log("ENCOUNTER");
  var dist = closeEnough();
  //console.log("dist: " + dist);
  if (dist != -1) { //&& Math.random() < .5) {
    //get a pokemon from API
    //get text, sprite, etc
    var contentString = "Filler stuff for now";
    var sprite = "http://www.stuycs.org/_/rsrc/1506974930674/config/customLogo.gif?revision=2";
    infoWindow = new google.maps.InfoWindow({
      content:
        "<div style='float:left'><img src='" +
        sprite +
        "'></div><div style='float:right; padding: 10px;'>" +
        contentString
    });
    infoWindow.setPosition(dist);
    infoWindow.open(map);
    if (google.maps.geometry.spherical.computeDistanceBetween(map.getCenter(),
                                                              dist) > 50) {
      console.log("A");
      infoWindow.close(); 
    }
  }
}
