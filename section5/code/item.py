import sqlite3
from sqlite3.dbapi2 import connect
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be blank!"
    )

    @jwt_required()     # Note* Parenthesis help.
    def get(self, name):
        #item = next(filter(lambda i: i['name'] == name, items), None) # This is the same as the commented code below.
        #return {'item':item}, 200 if item else 404 # Return a value and a status code.
        item = self.find_by_name(name)
        if item:
            return item, 200
        return {'message':"This item does not exist within this database!"}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('my_data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name = ?"
        item = cursor.execute(query, (name,))
        row = item.fetchone()
        connection.close()

        if row:
            return {'item': {'name':row[0], 'price':row[1]}}
        return None

    def post(self, name):
        #if next(filter(lambda item: item['name'] == name, items), None) is not None:
            #return {'message':f'Item {name} already exists!'}, 400
        #payload = request.get_json() # I could set force = True to force the content type to be JSON, however this is risky and should be avoided. Otherwise, I should set silent = True.
        #payload = Item.parser.parse_args()
        #item = {'name':name, 'price':payload['price']}
        #items.append(item)
        #return item, 201
        if self.find_by_name(name):
            return {'message': 'This item already exists within the database!'}, 409
        
        connection = sqlite3.connect('my_data.db')
        cursor = connection.cursor()
        data = Item.parser.parse_args()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (name, data['price']))

        connection.commit()
        connection.close()

        return {'name':name, 'price':data['price']}, 201

    def put(self, name):
        #item = next(filter(lambda item: item['name'] == name, items), None) 
        #status_code = 200 if item else 201
        #payload = request.get_json()
        #payload = Item.parser.parse_args()

        #if item is None:
            #item = {'name':name, 'price':payload['price']}
            #items.append(item)
        #else:
            #item.update(payload)
        #return item, status_code
        connection = sqlite3.connect('my_data.db')
        cursor = connection.cursor()
        data = self.parser.parse_args()
        item_exists = self.find_by_name(name)
        query = "UPDATE items SET price = ? WHERE name = ?" if item_exists else "INSERT INTO items VALUES (?, ?)"

        if item_exists:
            cursor.execute(query, (data['price'], name))
        else:
            cursor.execute(query, (name, data['price']))
        
        status_code = 200 if item_exists else 201
        connection.commit()
        connection.close()

        return {'name':name, 'price':data['price']}, status_code

    def delete(self, name):
        #global items
        #items = list(filter(lambda x:x['name'] != name, items))
        #return {'message':'Success!'}, 410
        connection = sqlite3.connect('my_data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name = ?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message':'Success!'}, 410

class ItemList(Resource):
    def get(self):
        #return {'items':items}, 200
        connection = sqlite3.connect('my_data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result.fetchall():
            items.append({'name':row[0], 'price':row[1]})

        connection.close()

        return {'items':items}
