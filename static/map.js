var map;
var activewindow;

function initMap() {
	bounds  = new google.maps.LatLngBounds();
	map = new google.maps.Map(document.getElementById('map'), {
		zoom: 10,
		center: {'lat': 43.6532, 'lng': -79.3832}
	});
}

// 		<p> Open Now: ${restaurant.opening_hours.open_now} </p>
function iwSetContent(restaurant){
	return `<h3> ${restaurant.name} </h3>
		<p> Rating: ${restaurant.rating} ⭐️ </p>
		<p> Price: ${restaurant.price_level} </p>
		<a href= '${restaurant.url}'> Open in Google Maps </a>`;
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

// GET is the default method, so we don't need to set it
fetch('/test')
	.then(function (response) {
			return response.json();
		}).then(function (dct) {
			for (var restaurant in dct) {
				console.log(dct[restaurant]);
				placeMarker(dct[restaurant]);
			};
	// .catch() {}
	});