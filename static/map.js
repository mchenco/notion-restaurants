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

	var chicago = {lat: 41.850, lng: -87.650};
	var controlUI = document.getElementById('control-ui');
	controlUI.addEventListener('click', function() {
	  map.setCenter(chicago)
	});

  var centerControlDiv = document.getElementById('control-div');
  var centerControl = new CenterControl(centerControlDiv, map);

  centerControlDiv.index = 1;
  map.controls[google.maps.ControlPosition.BOTTOM_RIGHT].push(centerControlDiv);

	google.maps.event.addListener(map, 'bounds_changed', function() {
        this.north = map.getBounds().getNorthEast().lat();  
	    this.east = map.getBounds().getNorthEast().lng();
	    this.south = map.getBounds().getSouthWest().lat();  
	    this.west = map.getBounds().getSouthWest().lng();
     });

	google.maps.event.addListener(map, 'idle', function() {
		getRestaurants(this.north, this.east, this.south, this.west);
	});
};

function CenterControl(controlDiv, map) {
  var controlUI = document.getElementById('control-ui');
  var controlText = document.getElementById('control-text');

  controlUI.addEventListener('click', function() {
    location.href = "/";
  });

};

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
};

// <p> <b> Open Now: </b> ${restaurant.opening_hours.open_now} </p>
function iwSetContent(restaurant){
	var picImg = "data:image/png;base64," + restaurant.photos;
	console.log(restaurant.price_level)
	restaurant.price_level = restaurant.price_level ? restaurant.price_level : 0;
	return `
		<div id="iw-wrapper">
			<div id="iw-header">
				<img id="iw-photo" src=${picImg}>
			</div>
			<p id=iw-heading-text>${restaurant.name} </p>
			<div id="iw-details">
				<div id="iw-rating-header" class="iw-details-header">
					Rating
				</div>
				<div id=iw-rating class="iw-details-text">
			        <div class="Stars" style="--rating: ${restaurant.rating};"> </div>
			        ${restaurant.rating}
				</div>
				<div id=iw-price-header class="iw-details-header">
					Price
				</div>
				<div id=iw-price class="iw-details-text">
					<div class="Dollars" style="--rating: ${restaurant.price_level};"> </div>
					${restaurant.price_level}
				</div>
				<button id="iw-link-button" onclick="window.location.href='${restaurant.url}';"> <i class="fas fa-location-arrow"></i> </button>
			</div>
		</div>
	`;
};

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