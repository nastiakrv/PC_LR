from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
import sys
import os
from datetime import datetime
from flask_migrate import Migrate

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from extensions import db  # Імпортуємо db з extensions.py
from db import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Ініціалізуємо db з додатком
db.init_app(app)

migrate = Migrate(app, db)  # Ініціалізуємо Flask-Migrate

api = Api(app)

user_parser = reqparse.RequestParser()
user_parser.add_argument('full_name', type=str, required=True, help='Full name is required')
user_parser.add_argument('email', type=str, required=True, help='Email is required')

userFields = {
    'id': fields.Integer,
    'full_name': fields.String,
    'email': fields.String,
}

class UserResource(Resource):
    @marshal_with(userFields)
    def get(self, id=None):
        if id:
            user = User.query.get(id)
            if not user:
                abort(404, message="User not found")
            return user
        else:
            users = User.query.all()
            return users

    @marshal_with(userFields)
    def post(self):
        args = user_parser.parse_args()
        new_user = User(full_name=args['full_name'], email=args['email'])
        db.session.add(new_user)
        db.session.commit()
        return new_user, 201

    @marshal_with(userFields)
    def patch(self, id):
        user = User.query.get(id)
        if not user:
            abort(404, message="User not found")

        args = user_parser.parse_args()
        user.full_name = args['full_name']
        user.email = args['email']

        db.session.commit()
        return user, 200

    def delete(self, id):
        user = User.query.get(id)
        if not user:
            abort(404, message="User not found")
        db.session.delete(user)
        db.session.commit()
        return {'message': f'User {id} deleted'}, 200
    
    
api.add_resource(UserResource, '/users', '/users/<int:id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
