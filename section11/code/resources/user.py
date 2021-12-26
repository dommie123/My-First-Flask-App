import sqlite3
from flask_restful import Resource, reqparse

from models.user_model import User

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be blank!"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be blank!"
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        if User.find_by_username(data['username']):
            return {'message':'This user already exists in the database!'}, 409

        user = User(**data)
        user.save_user()

        return {'message':'User created successfully!'}, 201

class RUser(Resource):
    @classmethod
    def get(cls, user_id):
        user = User.find_by_id(user_id)
        if not user:
            return {'message':'User not found'}
        return user.json()
    
    @classmethod
    def delete(cls, user_id):
        user = User.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted'}, 200