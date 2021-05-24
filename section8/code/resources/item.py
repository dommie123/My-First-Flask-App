from sqlite3.dbapi2 import connect
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item_model import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="This item must belong to a store!"
    )
    @jwt_required()     # Note* Parenthesis help.
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message':"This item does not exist within this database!"}, 404

    def post(self, name):
        ItemModel.find_by_name(name)
        if ItemModel.find_by_name(name):
            return {'message': 'This item already exists within the database!'}, 409
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save()
        except:
            return {'message':'An error has occurred while creating this item!'}, 500

        return item.json(), 201 

    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)
        status_code = 202
        if item is None:
            item = ItemModel(name, **data)
            status_code = 201
        else:
            item.price = data['price']
            status_code = 200
        
        item.save()
        return item.json(), status_code

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_item()
        return {'message':'Success!'}, 410
        

class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}, 200
