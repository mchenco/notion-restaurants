var map;
var activewindow;
var north, east, south, west;

function initMap() {
	var city = $('#city').attr('content');
	var geocoder = new google.maps.Geocoder();

	geocoder.geocode({'address': city}, function(results, status) {
    if (status === 'OK') {
    	map.setCenter(results[0].geometry.location);
    } else {
    	alert('Geocode was not successful for the following reason: ' + status);
    }
  });

	bounds  = new google.maps.LatLngBounds();
	map = new google.maps.Map(document.getElementById('map'), {
		zoom: 13,
		center: {'lat': 43.6532, 'lng': -79.3832}
	});

	google.maps.event.addListener(map, 'bounds_changed', function() {
        this.north = map.getBounds().getNorthEast().lat();  
	    this.east = map.getBounds().getNorthEast().lng();
	    this.south = map.getBounds().getSouthWest().lat();  
	    this.west = map.getBounds().getSouthWest().lng();
     });

	google.maps.event.addListener(map, 'idle', function() {
		getRestaurants(this.north, this.east, this.south, this.west);
	});
}

function placeMarker(restaurant) {
	var marker = new google.maps.Marker({
		position: {'lat': restaurant.lat, 'lng': restaurant.lng},
		map: map,
		title: restaurant.name
	});

	var infowindow = new google.maps.InfoWindow({
	    	content: iwSetContent(restaurant)
	    });

	marker.addListener('click', function() {
		if (activewindow) {
			activewindow.close();
		};
		infowindow.open(map, marker);
		activewindow = infowindow;
	});
}

// <p> <b> Open Now: </b> ${restaurant.opening_hours.open_now} </p>
function iwSetContent(restaurant){
	return `<p id=iw-heading>${restaurant.name} </p>
		<hr class="solid">
		<p id=iw-rating class="par"> <b> Rating: </b> ${restaurant.rating} ⭐️ </p>
		<p id=iw-price class="par"> <b> Price: </b>${restaurant.price_level} 💸 </p>
		<a id=iw-url class="par" href= "${restaurant.url}"> Google Maps </a>`;
}

function getRestaurants(north, east, south, west) {
	fetch('/test', {
		method: 'POST',
		headers: { 'Content-Type':'application/json' },
		body: JSON.stringify({
			north: north,
			east: east,
			south: south,
			west: west
		})
	}).then(function (response) {
			return response.json();
		}).then(function (dct) {
			for (var restaurant in dct) {
				placeMarker(dct[restaurant]);
			};
	// .catch() {}
	});
};