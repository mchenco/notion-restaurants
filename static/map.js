var map;

function initMap() {
	var apple = {lat: 37.3327, lng: -122.0053};

	map = new google.maps.Map(document.getElementById('map'), {
		zoom: 11,
		center: apple
	});

	var marker = new google.maps.Marker({
		position: apple,
		map: map,
		icon: {
			url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
		},
		title: 'Apple Park'
	});
}

function placeMarker(coords) {
	var latLng = new google.maps.LatLng(
		coords.geometry.location.lat,
		coords.geometry.location.lng
	);

	var marker = new google.maps.Marker({
		position: latLng,
		map: map,
		title: coords.formatted_address
	});
}

// GET is the default method, so we don't need to set it
fetch('/test')
	.then(function (response) {
			return response.json();
		}).then(function (all_addr) {
			// for (x of all_addr) {
			// 	console.log(x[0]);
			// 	placeMarker(x[0]);
			// };
	// .catch() {}
	});