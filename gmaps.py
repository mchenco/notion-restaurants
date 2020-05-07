import os

import base64
import requests


def search(searchword):
	payload = {
		'key': os.environ.get('GMAPS_KEY'),
		'input': searchword,
		'inputtype': 'textquery',
		# 'locationbias': 'ipbias',
		'fields': 'formatted_address,geometry,icon,name,place_id'
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
		'fields': 'url,price_level,rating,opening_hours,photos',
	}
	r = requests.get(
		'https://maps.googleapis.com/maps/api/place/details/json?',
		params=payload
	)
	result = r.json()
	photoref = result['result']['photos'][0]['photo_reference']
	photo = photo_search(photoref)
	result['result']['photos'] = photo
	return result


def photo_search(photoreference):
	payload = {
		'key': os.environ.get('GMAPS_KEY'),
		'photoreference': photoreference,
		'maxwidth': 250
	}
	r = requests.get(
		'https://maps.googleapis.com/maps/api/place/photo?',
		params=payload
	)
	if r.status_code == 200:
		b64string = str(base64.b64encode(r.content).decode("utf-8"))
		return b64string
