var map;

function initMap() {
	bounds  = new google.maps.LatLngBounds();
	map = new google.maps.Map(document.getElementById('map'), {
		zoom: 10,
		center: {'lat': 43.6532, 'lng': -79.3832}
	});
}

function placeMarker(lat, lng) {
	var marker = new google.maps.Marker({
		position: {'lat': lat, 'lng': lng},
		map: map
		// title: coords.formatted_address
	});
}

// GET is the default method, so we don't need to set it
fetch('/test')
	.then(function (response) {
			return response.json();
		}).then(function (dct) {
			for (var restaurant in dct) {
				lat = dct[restaurant].lat;
				lng = dct[restaurant].lng;
				placeMarker(lat, lng);
			};
	// .catch() {}
	});