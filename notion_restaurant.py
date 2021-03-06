import os

import gmaps
from notion.client import NotionClient


class NotionDB:
	def __init__(self):
		self.client = NotionClient(os.environ.get('NOTION_KEY'))
		self.cv = self.client.get_collection_view(os.environ.get('RESTAURANT_DB'))
		self.dct = dict()

		self.update_addresses()
		return

	def query(self):
		return self.cv.default_query().execute()

	# update coordinates of addresses
	def update_addresses(self):
		filter_params = [{
			'property': 'address',
			'comparator': 'is',
			'value': ''
		}]

		filter_result = self.cv.build_query(filter=filter_params).execute()

		for row in filter_result:
			# only update results that don't have info populated
			if row.title and not row.place_id:
				data = gmaps.search(row.title)
				if data['status'] == 'OK':
					info = data['candidates'][0]
					row.address = info['formatted_address']
					row.lat = info['geometry']['location']['lat']
					row.lng = info['geometry']['location']['lng']
					row.marker_icon = info['icon']
					row.icon = info['icon']
					row.place_id = info['place_id']
		return

	# construct a dict -> json object
	def get_info(self, coords):
		result = self.query()

		for row in result:
			if row.place_id and \
				row.lat <= coords['north'] and row.lat >= coords['south'] and \
				row.lng >= coords['west'] and row.lng <= coords['east']:

				json_string = {
					'name': row.name,
					'address': row.address,
					'lat': row.lat,
					'lng': row.lng,
					# 'marker_icon' : row.marker_icon,
					'place_id': row.place_id
				}
				self.dct[row.place_id] = json_string

				details = gmaps.detail_search(row.place_id)
				if details['status'] == 'OK':
					for x in details['result']:
						self.dct[row.place_id].update({x: details['result'][x]})

		return self.dct
