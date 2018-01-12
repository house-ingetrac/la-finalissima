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
    window.addEventListener('keydown', keyDownHandler);
    window.addEventListener('keyup', keyUpHandler);
    movement = setInterval(move, 25);
    //heater();
}

function genRandPoints(numPoints, lat, long) {
    var ret = [];
    var randLat;
    var randLong;
    var location = {lat, long};
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
    heatPoints = new google.maps.MVCArray(heatLocations);

    heatmap = new google.maps.visualization.HeatmapLayer({
        data: heatPoints,
        map: map,
        radius: 30
    });
  var points = getPoints();
  for (var i = 0; i < points.length; i ++) {
    heatPoints.push(points[i]);
  }
    heatmap.setMap(map);
}

function encounter() {
    //if (pkmnLocations.indexOf(map.getCenter()) >= 0) { //doesn't account for if it's "close enough"
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
    infoWindow.setPosition(loc);
    infoWindow.open(map);
    //}
}
