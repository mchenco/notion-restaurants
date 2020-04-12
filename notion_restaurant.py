import os 

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from notion.client import NotionClient
import googlemaps
import requests

from app import db

class NotionDB:
	def __init__(self):
		self.client = NotionClient(os.environ.get('NOTION_KEY'))
		self.cv = self.client.get_collection_view(os.environ.get('RESTAURANT_DB'))
		self.dct = dict()
		return

	def query(self):
		return self.cv.default_query().execute()

	def update_addresses(self):
		filter_params = [{
		    'property': 'address',
		    'comparator': 'is',
		    'value': ''
		}]

		# filter_params =  {
  #       "filters":[ 
  #           { 
  #               "filter":{ 
  #                   "property":"address",
  #                   "comparator":"is",
  #                   "value":''
  #               },
  #           },
  #           { 
  #               "filter":{ 
  #                   "property":"title",
  #                   "comparator":"is_not",
  #                   "value": ''
  #               },
  #           }
  #       ],
  #       "operator":"and"
  #   }

		filter_result = self.cv.build_query(filter=filter_params).execute()

		for row in filter_result:
			# filter queries aren't working so xtra checks :(
			if row.title and row.address == '':
				payload = {
					'key': os.environ.get('GMAPS_KEY'),
					'input': row.title,
					'inputtype': 'textquery',
					'locationbias': 'ipbias',
					'fields': 'formatted_address,geometry,icon,name,photos,place_id'
				
				}
				r = requests.get(
					'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?',
					params=payload
				)
				data = r.json()
				if data['status'] == 'OK':
					info = data['candidates'][0]
					addr = info['formatted_address']
					row.address = addr
					# self.dct[info['name']] = info
					restaurant = Restaurant(info)
					db.session.add(restaurant)
					db.session.commit()
					return

	def get_geo_addresses(self):
		query = self.query()
		addresses = []

		for row in query:
			if row.address != '':
				addresses.append(self.geocode(row.address))
		return addresses

	def geocode(self, addr):
		gmaps = googlemaps.Client(os.environ.get('GMAPS_KEY'))
		return gmaps.geocode(addr)

class Restaurant(db.Model):
	__tablename__ = 'restaurant_data'
	place_id = db.Column(db.String(), primary_key=True)
	name = db.Column(db.String(120))
	formatted_address = db.Column(db.String(120))
	# photos = db.Column(db.String(120))
	lat = db.Column(db.Float())
	lng = db.Column(db.Float())
	icon = db.Column(db.String(120))
	# json_data = db.Column(db.JSON, unique=True)

	def __init__(self, info):
		print ('initializing restaurant objjjjjjj')
		self.place_id = info['place_id']
		self.name = info['name']
		self.formatted_address = info['formatted_address']
		self.lat = info['geometry']['location']['lat']
		self.lng = info['geometry']['location']['lng']
		self.icon = info['icon']
