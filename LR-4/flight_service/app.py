from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flask_migrate import Migrate  # Додано Flask-Migrate
from extensions import db
from db import Flight
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Спільна база даних
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)  # Ініціалізація Flask-Migrate
api = Api(app)

flight_parser = reqparse.RequestParser()
flight_parser.add_argument('origin', type=str, required=True, help='Origin is required')
flight_parser.add_argument('destination', type=str, required=True, help='Destination is required')
flight_parser.add_argument('departure_time', type=str, required=True, help='Departure time is required')
flight_parser.add_argument('arrival_time', type=str, required=True, help='Arrival time is required')
flight_parser.add_argument('base_price', type=float, required=True, help='Base price is required')
flight_parser.add_argument('seats_available', type=int, required=True, help='Seats available is required')

flight_fields = {
    'id': fields.Integer,
    'origin': fields.String,
    'destination': fields.String,
    'departure_time': fields.String,
    'arrival_time': fields.String,
    'base_price': fields.Float,
    'seats_available': fields.Integer,
}

class FlightResource(Resource):
    @marshal_with(flight_fields)
    def get(self, id=None):
        if id:
            flight = Flight.query.get(id)
            if not flight:
                abort(404, message="Flight not found")
            return flight
        else:
            flights = Flight.query.all()
            return flights

    @marshal_with(flight_fields)
    def post(self):
        args = flight_parser.parse_args()
        new_flight = Flight(
            origin=args['origin'],
            destination=args['destination'],
            departure_time=datetime.fromisoformat(args['departure_time']),
            arrival_time=datetime.fromisoformat(args['arrival_time']),
            base_price=args['base_price'],
            seats_available=args['seats_available']
        )
        db.session.add(new_flight)
        db.session.commit()
        return new_flight, 201

    def delete(self, id):
        flight = Flight.query.get(id)
        if not flight:
            abort(404, message="Flight not found")
        db.session.delete(flight)
        db.session.commit()
        return {'message': f'Flight {id} deleted'}, 200

api.add_resource(FlightResource, '/flights', '/flights/<int:id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)