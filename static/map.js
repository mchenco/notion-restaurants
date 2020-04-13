var map;
var activewindow;

function initMap() {
	bounds  = new google.maps.LatLngBounds();
	map = new google.maps.Map(document.getElementById('map'), {
		zoom: 10,
		center: {'lat': 43.6532, 'lng': -79.3832}
	});
}

function placeMarker(restaurant) {
	lat = restaurant.lat;
	lng = restaurant.lng;

	var infowindow = new google.maps.InfoWindow({
    	content: restaurant.name
    });

	var marker = new google.maps.Marker({
		position: {'lat': lat, 'lng': lng},
		map: map,
		title: restaurant.name
	});

	marker.addListener('click', function() {
		if (activewindow) {
			activewindow.close();
		};
		infowindow.open(map, marker);
		activewindow = infowindow;
	});
}

// GET is the default method, so we don't need to set it
fetch('/test')
	.then(function (response) {
			return response.json();
		}).then(function (dct) {
			for (var restaurant in dct) {
				placeMarker(dct[restaurant]);
			};
	// .catch() {}
	});