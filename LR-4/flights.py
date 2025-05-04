#from api import db
from extensions import db
from datetime import datetime

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