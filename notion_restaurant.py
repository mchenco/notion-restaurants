import os 

from notion.client import NotionClient
import googlemaps
import requests

class NotionDB:
	def __init__(self):
		self.client = NotionClient(os.environ.get('NOTION_KEY'))
		self.cv = self.client.get_collection_view(os.environ.get('RESTAURANT_DB'))
		self.update_addresses()
		return

	"""
	i don't see a way to create a new prop from the library
	falling on user to ensure all properties are there
	"""
	# def init_db(self):
	# 	for row in self.query():
	# 		try:
	# 			print(row.get_all_properties())
	# 		except:
	# 			print('nope do not exist')

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
	
	#update coordinates of addresses
	def update_addresses(self):
		filter_params = [{
		    'property': 'address',
		    'comparator': 'is',
		    'value': ''
		}]

		filter_result = self.cv.build_query(filter=filter_params).execute()

		for row in filter_result:
			# only update results that don't have info populated
			if row.title and not row.lat:
				data = self.gmaps_search(row.title)
				if data['status'] == 'OK':
					info = data['candidates'][0]
					addr = info['formatted_address']
					row.address = addr
					row.lat = info['geometry']['location']['lat']
					row.lng = info['geometry']['location']['lng']
					row.icon = info['icon']
					row.place_id = info['place_id']
		return

	def get_info(self):
		#construct a dict -> json object
		dct = dict()
		result = self.query()

		for row in result:
			if row.address:
				json_string = {
					'name' : row.name,
					'address' : row.address,
					'lat' : row.lat,
					'lng' : row.lng,
					'icon' : row.icon,
					'place_id' : row.place_id
				}
				dct[row.place_id] = json_string

		return dct
