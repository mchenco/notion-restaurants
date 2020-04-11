import os 

from notion.client import NotionClient
import googlemaps
from datetime import datetime

def get_notion_db():
	client = NotionClient(os.environ.get('NOTION_KEY'))
	cv = client.get_collection_view(os.environ.get('RESTAURANT_DB'))
	return cv.default_query().execute()

def add_addresses(cv):
	for row in cv:
		print(row.title)
		
	return


# def get_addresses():
# 	addresses = []
# 	data = get_notion_db()
# 	lst = [row for row in data if row.title] #removes empties
# 	for row in lst:
# 		raw_addr = row.title
# 		addr = str(row.title.split('|')[0])
# 		addresses.append(addr)
# 	return addresses

# 	#### yo add db to remove duplicates ??/
# 	### hash table this bitch ??

# def geocode(addr):
# 	gmaps = googlemaps.Client(os.environ.get('GMAPS_KEY'))
# 	return gmaps.geocode(addr)
