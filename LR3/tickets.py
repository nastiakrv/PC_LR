#from api import db
from extensions import db

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'), nullable=False)
    
    has_baggage = db.Column(db.Boolean, default=False)
    price_paid = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Ticket ID {self.id} - User {self.user_id}, Flight {self.flight_id}>'
