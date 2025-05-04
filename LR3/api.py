from flask import Flask
from extensions import db
#from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from resources import UserResource, FlightResource, TicketResource


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#db = SQLAlchemy(app)
db.init_app(app)

api = Api(app)

@app.route('/')

def home():
    return '<h1>LR-3</h1>'

api.add_resource(UserResource, '/users', '/users/<int:id>')
api.add_resource(FlightResource, '/flights', '/flights/<int:id>')
api.add_resource(TicketResource, '/tickets', '/tickets/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
