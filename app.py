import os

import notion_restaurant
from flask import Flask, jsonify, request, render_template
from flask_heroku import Heroku

app = Flask(__name__)
heroku = Heroku(app)

@app.route('/')
def index():
	return render_template('index.html', token = os.environ.get('GMAPS_LINK'))
	

@app.route('/test', methods=['GET', 'POST'])
def test():
	cv = notion_restaurant.NotionDB()

	# POST request
	if request.method == 'POST':
		print('Incoming ..')
		print(request.get_json())
		return 'OK', 200

	# GET request
	else:
		dct = cv.get_info()
		return jsonify(dct)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)