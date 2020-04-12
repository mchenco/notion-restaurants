import os 

from notion.client import NotionClient
import googlemaps
import requests

class NotionDB:
	def __init__(self):
		self.client = NotionClient(os.environ.get('NOTION_KEY'))
		self.cv = self.client.get_collection_view(os.environ.get('RESTAURANT_DB'))
		self.dct = dict()
		self.add_all_addresses()
		return

	def query(self):
		return self.cv.default_query().execute()

	def gmaps_search(self, searchword):
		payload = {
			'key': os.environ.get('GMAPS_KEY'),
			'input': searchword,
			'inputtype': 'textquery',
			'locationbias': 'ipbias',
			'fields': 'formatted_address,geometry,icon,name,photos,place_id'
		}
		r = requests.get(
			'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?',
			params=payload
		)
		return r.json()

	# def update_addresses(self):
	# 	filter_params = [{
	# 	    'property': 'address',
	# 	    'comparator': 'is',
	# 	    'value': ''
	# 	}]

	# 	filter_result = self.cv.build_query(filter=filter_params).execute()

	# 	for row in filter_result:
	# 		# filter queries aren't working so xtra checks :(
	# 		if row.title and row.address == '':
	# 			data = self.gmaps_search(row.title)
	# 			if data['status'] == 'OK':
	# 				info = data['candidates'][0]
	# 				addr = info['formatted_address']
	# 				row.address = addr
	# 				self.dct[info['name']] = info
	# 	return

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
					self.dct[info['place_id']] = info

	def get_info(self):
		return self.dct

class Restaurant():
	def __init__(self, info):
		self.place_id = info['place_id']
		self.name = info['name']
		self.formatted_address = info['formatted_address']
		self.lat = info['geometry']['location']['lat']
		self.lng = info['geometry']['location']['lng']
		self.icon = info['icon']
		# self.photos =