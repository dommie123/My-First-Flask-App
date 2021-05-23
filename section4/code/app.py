from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'Ass'
api = Api(app)

jwt = JWT(app, authenticate, identity) # Creates a new endpoint "/auth"

items = []

#class Student(Resource):
    #def get(self, name):
        #return {'student':name}
    #def post(self):
    #def put(self):
    #def delete(self):
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be blank!"
    )

    @jwt_required()     # Note* Parenthesis help.
    def get(self, name):
        item = next(filter(lambda i: i['name'] == name, items), None) # This is the same as the commented code below.
        #for item in items:
            #if item['name'] == name:
                #return {'message':'This item already exists!'}, 409
        return {'item':item}, 200 if item else 404 # Return a value and a status code.

    def post(self, name):
        if next(filter(lambda item: item['name'] == name, items), None) is not None:
            return {'message':f'Item {name} already exists!'}, 400
        #payload = request.get_json() # I could set force = True to force the content type to be JSON, however this is risky and should be avoided. Otherwise, I should set silent = True.
        payload = Item.parser.parse_args()
        item = {'name':name, 'price':payload['price']}
        items.append(item)
        return item, 201

    def put(self, name):
        item = next(filter(lambda item: item['name'] == name, items), None) 
        status_code = 200 if item else 201
        #payload = request.get_json()
        payload = Item.parser.parse_args()

        if item is None:
            item = {'name':name, 'price':payload['price']}
            items.append(item)
        else:
            item.update(payload)
        return item, status_code

    def delete(self, name):
        global items
        items = list(filter(lambda x:x['name'] != name, items))
        return {'message':'Success!'}, 410

class ItemList(Resource):
    def get(self):
        return {'items':items}, 200

# This is the only way to access the Student class using the API.
#api.add_resource(Student, '/student/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

# If i wish to display errur messages to make debugging easier, we can 
# set the debug parameter equal to True.
app.run(port=5000, debug=True)