#from api import db
from extensions import db
#from tickets import Ticket


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    tickets = db.relationship('Ticket', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.full_name}, email={self.email}>'
