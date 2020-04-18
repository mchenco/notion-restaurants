import os

import requests
import googlemaps

def search(searchword):
	payload = {
		'key': os.environ.get('GMAPS_KEY'),
		'input': searchword,
		'inputtype': 'textquery',
		# 'locationbias': 'ipbias',
		'fields': 'formatted_address,geometry,icon,name,photos,place_id'
	}
	r = requests.get(
		'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?',
		params=payload
	)
	return r.json()

def detail_search(place_id):
	payload = {
		'key': os.environ.get('GMAPS_KEY'),
		'place_id': place_id,
		'fields': 'url,price_level,rating,opening_hours' #review made it slow
	}
	r = requests.get(
		'https://maps.googleapis.com/maps/api/place/details/json?',
		params=payload
	)
	return r.json()