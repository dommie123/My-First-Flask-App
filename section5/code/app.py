from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'Ass'
api = Api(app)

jwt = JWT(app, authenticate, identity) # Creates a new endpoint "/auth"

#items = []

# This is the only way to access the Student class using the API.
#api.add_resource(Student, '/student/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

# If i wish to display errur messages to make debugging easier, we can 
# set the debug parameter equal to True.
app.run(port=5000, debug=True)