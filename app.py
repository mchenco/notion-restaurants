import os

import notion_restaurant
from flask import Flask, jsonify, request, render_template
from flask_heroku import Heroku
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
heroku = Heroku(app)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/restaurant_data'

# class Restaurant(db.Model):
# 	__tablename__ = 'restaurant_data'
# 	name = db.Column(db.String(120), primary_key=True)
# 	json_data = db.Column(JSON, unique=True)

# 	def __init__(self, info):
# 		self.name = info['name']
# 		self.json_data = info


@app.route('/')
def hello():
	return render_template('index.html', token = os.environ.get('GMAPS_LINK'))
	

@app.route('/test', methods=['GET', 'POST'])
def test():
	cv = notion_restaurant.NotionDB()
	cv.update_addresses()

	# POST request
	if request.method == 'POST':
		print('Incoming ..')
		print(request.get_json())
		return 'OK', 200

	# GET request
	else:
		addresses = cv.get_geo_addresses()
		return jsonify(addresses)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)