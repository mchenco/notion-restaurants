import os 

from notion.client import NotionClient
import googlemaps
import requests

class NotionDB:
	def __init__(self):
		self.client = NotionClient(os.environ.get('NOTION_KEY'))
		self.cv = self.client.get_collection_view(os.environ.get('RESTAURANT_DB'))
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
			# filter queries aren't working so xtra checks :()
			if row.title and row.address == '':
				print(row.title)
				payload = {
					'key': os.environ.get('GMAPS_KEY'),
					'input': row.title,
					'inputtype': 'textquery',
					'locationbias': 'ipbias',
					'fields': ['formatted_address', 'geometry', 'icon', 'name', 'photos', 'place_id']
				}
				r = requests.get(
					'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?',
					params=payload
				)
				data = r.json()
				if data['status'] == 'OK':
					addr = data['candidates'][0]['formatted_address']
					row.address = addr
		return


	# def get_addresses(self):
	# 	addresses = []
	# 	data = get_notion_db()
	# 	lst = [row for row in data if row.title] #removes empties
	# 	for row in lst:
	# 		raw_addr = row.title
	# 		addr = str(row.title.split('|')[0])
	# 		addresses.append(addr)
	# 	return addresses

		#### yo add db to remove duplicates ??/
		### hash table this bitch ??

	# def geocode(addr):
	# 	gmaps = googlemaps.Client(os.environ.get('GMAPS_KEY'))
	# 	return gmaps.geocode(addr)
