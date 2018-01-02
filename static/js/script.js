var map, heatmap, infoWindow, loc, dir, movement;
var mapDiv = document.getElementById('map');

function move() {
    //console.log('moving');
    loc.lat = map.getCenter().lat();
    loc.lng = map.getCenter().lng();
    loc.lat += dir.lat;
    loc.lng += dir.lng;
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
    heatmap = new google.maps.visualization.HeatmapLayer({
        data: getPoints(),
        map: map
    });
    window.addEventListener('keydown', keyDownHandler);
    window.addEventListener('keyup', keyUpHandler);
    movement = setInterval(move, 25);
    
}

function genRandPoints(numPoints, lat, long) {
  var ret = [];
  var randLat;
  var randLong;
  for (var i = 0; i < numPoints; i ++) {
    randLat = Math.random() * 0.001;
    randLong = Math.random() * 0.001;
    ret.push(new google.maps.LatLng(lat + randLat, long + randLong));
  }
  console.log(ret);
  return ret;
}

// Heatmap data: 500 Points
function getPoints() {
  return genRandPoints(20, 40.76, -73.99);
  //new google.maps.LatLng(37.751266, -122.403355)
}
