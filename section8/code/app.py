from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_data.db'
app.secret_key = 'Ass'
api = Api(app)

jwt = JWT(app, authenticate, identity) # Creates a new endpoint "/auth"

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

# If i wish to display errur messages to make debugging easier, we can 
# set the debug parameter equal to True.
# if __name__ == '__main__':
#     db.init_app(app)
#     app.run(port=5000, debug=True)