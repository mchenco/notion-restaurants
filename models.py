from app import db

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
		self.place_id = info['place_id']
		self.name = info['name']
		self.formatted_address = info['formatted_address']
		self.lat = info['geometry']['location']['lat']
		self.lng = info['geometry']['location']['lng']
		self.icon = info['icon']
