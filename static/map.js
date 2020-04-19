var map;
var activewindow;
var startlat;
var startlng;

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
		zoom: 10,
		center: {'lat': 43.6532, 'lng': -79.3832}
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

// fetch('/')
// 	.then(function (response) {
// 		console.log(response)
// 	})

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