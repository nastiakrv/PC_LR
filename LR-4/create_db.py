from api import app, db
from users import User
from flights import Flight
from tickets import Ticket

with app.app_context():
    db.create_all()
    print("DB created!")
