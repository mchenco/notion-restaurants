import os

import notion_restaurant
from flask import Flask, jsonify, request, render_template
app = Flask(__name__)

@app.route('/')
def hello():
	cv = notion_restaurant.get_notion_db()
	notion_restaurant.add_addresses(cv)
	return render_template('index.html', token = os.environ.get('GMAPS_LINK'))
	

# @app.route('/test', methods=['GET', 'POST'])
# def test():
# 	# POST request
# 	if request.method == 'POST':
# 		print('Incoming ..')
# 		print(request.get_json())
# 		return 'OK', 200

# 	# GET request
# 	else:
# 		# geocoded_addresses = []
# 		notion_restaurant.get_notion_db()
# 		# all_addr = notion_restaurant.get_addresses()
# 		# for addr in all_addr:
# 		# 	geocoded_addresses.append(notion_restaurant.geocode(addr))
# 		return jsonify(notion_restaurant.get_notion_db())


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)