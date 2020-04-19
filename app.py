import os

import notion_restaurant
import gmaps

from flask import Flask, jsonify, request, render_template, redirect, session
from flask_heroku import Heroku

app = Flask(__name__)
heroku = Heroku(app)

@app.route('/')
def index():
	return render_template('search.html')

@app.route('/', methods=['POST'])
def get_city():
	city = request.form.get('city')
	
	return render_template(
		'index.html',
		city=city,
		token=os.environ.get('GMAPS_LINK')
	)

@app.route('/test', methods=['GET', 'POST'])
def test():
	cv = notion_restaurant.NotionDB()

	# POST request
	if request.method == 'POST':
		coords = request.get_json()

	# GET request
	dct = cv.get_info(coords)
	return jsonify(dct)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)