import os 

from models import Restaurant

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from notion.client import NotionClient
import googlemaps
import requests

from app import db

class NotionDB:
	def __init__(self):
		self.client = NotionClient(os.environ.get('NOTION_KEY'))
		self.cv = self.client.get_collection_view(os.environ.get('RESTAURANT_DB'))
		return

	def query(self):
		return self.cv.default_query().execute()

	def add_address_to_db(self, info):
		restaurant = Restaurant(info)

		try:
			db.session.add(restaurant)
			db.session.commit()
		except IntegrityError:
			db.session.rollback()
		return

	def gmaps_search(self, search):
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
		return r.json()

	#initialize database
	def add_all_addresses(self):
		filter_params = [{
		    'property': 'address',
		    'comparator': 'is',
		    'value': ''
		}]

		filter_result = self.cv.build_query(filter=filter_params).execute()

		for row in filter_result:
			if row.title:
				data = self.gmaps_search(row.title)
				if data['status'] == 'OK':
					info = data['candidates'][0]
					self.add_address_to_db(info)
		return
	
	#only add new restaurants, ones that aren't in db
	def update_addresses(self):
		filter_params = [{
		    'property': 'address',
		    'comparator': 'is',
		    'value': ''
		}]

		filter_result = self.cv.build_query(filter=filter_params).execute()

		for row in filter_result:
			# filter queries aren't working so xtra checks :(
			if row.title and row.address == '':
				data = self.gmaps_search(row.title)
				if data['status'] == 'OK':
					info = data['candidates'][0]
					addr = info['formatted_address']
					row.address = addr
					# self.dct[info['name']] = info
					self.add_address_to_db(info)
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