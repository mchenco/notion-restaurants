import os

import notion_restaurant
from flask import Flask, jsonify, request, render_template
app = Flask(__name__)

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