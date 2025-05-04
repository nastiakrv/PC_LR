from extensions import db  # Використовуємо існуючий екземпляр db
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    tickets = db.relationship('Ticket', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.full_name}, email={self.email}>'

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'), nullable=False)
    has_baggage = db.Column(db.Boolean, default=False)
    price_paid = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Ticket ID {self.id} - User {self.user_id}, Flight {self.flight_id}>'

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    seats_available = db.Column(db.Integer, nullable=False)
    tickets = db.relationship('Ticket', backref='flight', lazy=True)

    def __repr__(self):
        return f'<Flight {self.origin} -> {self.destination}>'

    def calculate_price(self):
        total_seats = 100  # фіксоване значення
        days_before_departure = (self.departure_time - datetime.utcnow()).days
        time_factor = max(0, (14 - days_before_departure) / 14)
        seat_factor = 1 - (self.seats_available / total_seats)
        return round(self.base_price * (1 + 0.5 * (time_factor + seat_factor) / 2), 2)