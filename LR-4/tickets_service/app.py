from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flask_migrate import Migrate
from extensions import db
from db import Ticket

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Спільна база даних
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

ticket_parser = reqparse.RequestParser()
ticket_parser.add_argument('user_id', type=int, required=True, help='User ID is required')
ticket_parser.add_argument('flight_id', type=int, required=True, help='Flight ID is required')
ticket_parser.add_argument('has_baggage', type=bool, required=True, help='Has baggage is required')
ticket_parser.add_argument('price_paid', type=float, required=True, help='Price paid is required')

ticket_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'flight_id': fields.Integer,
    'has_baggage': fields.Boolean,
    'price_paid': fields.Float,
}

class TicketResource(Resource):
    @marshal_with(ticket_fields)
    def get(self, id=None):
        if id:
            ticket = Ticket.query.get(id)
            if not ticket:
                abort(404, message="Ticket not found")
            return ticket
        else:
            tickets = Ticket.query.all()
            return tickets

    @marshal_with(ticket_fields)
    def post(self):
        args = ticket_parser.parse_args()
        new_ticket = Ticket(
            user_id=args['user_id'],
            flight_id=args['flight_id'],
            has_baggage=args['has_baggage'],
            price_paid=args['price_paid']
        )
        db.session.add(new_ticket)
        db.session.commit()
        return new_ticket, 201

    def delete(self, id):
        ticket = Ticket.query.get(id)
        if not ticket:
            abort(404, message="Ticket not found")
        db.session.delete(ticket)
        db.session.commit()
        return {'message': f'Ticket {id} deleted'}, 200

api.add_resource(TicketResource, '/tickets', '/tickets/<int:id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)