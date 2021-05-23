from flask import Flask, jsonify, request

app = Flask(__name__)

# This is how I would store data locally if I am too poor to create a database.
stores = [
    {
        'name':'Kwik-E-Mart',
        'items': [
            {
                'name':'Dessert Dog',
                'price': 4.99
            }
        ]
    }
]

@app.route('/')
def home():
    return "Hello World!"

@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)

@app.route('/store/<string:name>')
def get_store(name: str):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'Store not found'})

@app.route('/store')
def get_stores():
    return jsonify({'stores':stores})


@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name: str):
    for store in stores:
        if store['name'] == name:
            request_data = request.get_json()       # This is how we receive JSON data in Flask.
            new_item = {
                'name':request_data['name'],
                'price':request_data['price']
            }
            store['items'].append(new_item)
            return jsonify({'items':store['items']}) # return list of items and take note of any changes
    return jsonify({'message':'Store not found!'})

@app.route('/store/<string:name>/item')
def get_item_in_store(name: str):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'Store Not Found!'})
             

app.run(port=5000)