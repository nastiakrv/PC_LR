from flask_restful import Resource, reqparse, fields, marshal_with, abort
#from api import db
from extensions import db
from users import User
from flights import Flight
from tickets import Ticket
from datetime import datetime

user_parser = reqparse.RequestParser()
user_parser.add_argument('full_name', type=str, required=True, help='Full name is required')
user_parser.add_argument('email', type=str, required=True, help='Email is required')

flight_parser = reqparse.RequestParser()
flight_parser.add_argument('origin', type=str, required=True, help='Origin is required')
flight_parser.add_argument('destination', type=str, required=True, help='Destination is required')
flight_parser.add_argument('departure_time', type=lambda x: datetime.fromisoformat(x), required=True, help='Departure time must be in ISO format (YYYY-MM-DDTHH:MM:SS)')
flight_parser.add_argument('arrival_time', type=lambda x: datetime.fromisoformat(x), required=True, help='Arrival time must be in ISO format (YYYY-MM-DDTHH:MM:SS)')
flight_parser.add_argument('base_price', type=float, required=True, help='Base price is required')
flight_parser.add_argument('seats_available', type=int, required=True, help='Seats available is required')

ticket_parser = reqparse.RequestParser()
ticket_parser.add_argument('user_id', type=int, required=True)
ticket_parser.add_argument('flight_id', type=int, required=True)
ticket_parser.add_argument('has_baggage', type=bool, required=False, default=False)
ticket_parser.add_argument('price_paid', type=float, required=False)

userFields = {
    'id': fields.Integer,
    'full_name': fields.String,
    'email': fields.String,
}

flightFields = {
    'id': fields.Integer,
    'origin': fields.String,
    'destination': fields.String,
    'departure_time': fields.DateTime(dt_format='iso8601'),
    'arrival_time': fields.DateTime(dt_format='iso8601'),
    'base_price': fields.Float,
    'seats_available': fields.Integer,
}

ticketFields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'flight_id': fields.Integer,
    'has_baggage': fields.Boolean,
    'price_paid': fields.Float,
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
    

# Flights
class FlightResource(Resource):
    @marshal_with(flightFields)
    def get(self, id=None):
        if id:
            flight = Flight.query.get(id)
            if not flight:
                abort(404, message="Flight not found")
            return flight
        else:
            flights = Flight.query.all()
            return flights

    @marshal_with(flightFields)
    def post(self):
        args = flight_parser.parse_args()
        new_flight = Flight(
            origin=args['origin'],
            destination=args['destination'],
            departure_time=args['departure_time'],
            arrival_time=args['arrival_time'],
            base_price=args['base_price'],
            seats_available=args['seats_available']
        )
        db.session.add(new_flight)
        db.session.commit()
        return new_flight, 201

    @marshal_with(flightFields)
    def patch(self, id):
        flight = Flight.query.get(id)
        if not flight:
            abort(404, message="Flight not found")

        args = flight_parser.parse_args()
        flight.origin = args['origin']
        flight.destination = args['destination']
        flight.departure_time = args['departure_time']
        flight.arrival_time = args['arrival_time']
        flight.base_price = args['base_price']
        flight.seats_available = args['seats_available']

        db.session.commit()
        return flight, 200

    def delete(self, id):
        flight = Flight.query.get(id)
        if not flight:
            abort(404, message="Flight not found")
        db.session.delete(flight)
        db.session.commit()
        return {'message': f'Flight {id} deleted'}, 200

#Tickets
class TicketResource(Resource):
    @marshal_with(ticketFields)
    def get(self, id=None):
        if id:
            ticket = Ticket.query.get(id)
            if not ticket:
                abort(404, message="Ticket not found")
            return ticket
        else:
            tickets = Ticket.query.all()
            return tickets

    @marshal_with(ticketFields)
    def post(self):
        args = ticket_parser.parse_args()
        user = User.query.get(args['user_id'])
        flight = Flight.query.get(args['flight_id'])

        if not user or not flight:
            abort(404, message="User or Flight not found")

        if flight.seats_available <= 0:
            abort(400, message="No seats available")

        price = flight.calculate_price()

        ticket = Ticket(user_id=user.id, flight_id=flight.id, price_paid=price) # add has_baggage
        flight.seats_available -= 1
        db.session.add(ticket)
        db.session.commit()

        return ticket, 201
    



    @marshal_with(ticketFields)
    def patch(self, id):
        ticket = Ticket.query.get(id)
        if not ticket:
            abort(404, message="Ticket not found")

        args = ticket_parser.parse_args()
        ticket.user_id = args['user_id']
        ticket.flight_id = args['flight_id']
        ticket.has_baggage = args['has_baggage']
        ticket.price_paid = args['price_paid']

        db.session.commit()
        return ticket, 200

    def delete(self, id):
        ticket = Ticket.query.get(id)
        if not ticket:
            abort(404, message="Ticket not found")
        db.session.delete(ticket)
        db.session.commit()
        return {'message': f'Ticket {id} deleted'}, 200
