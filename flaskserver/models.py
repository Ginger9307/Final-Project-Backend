from datetime import datetime
from email.policy import default
from flaskserver import db, ma
from flask_login import UserMixin


class Journeys_Users(db.Model):
    journey_id = db.Column(db.ForeignKey('journey.id'), primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    status = db.Column(db.String, default='True')

    journey = db.relationship('Journey', back_populates='passengers')
    passenger = db.relationship('User', back_populates='journeys')

    def __repr__(self):
        return f"JU('{self.journey}', '{self.passenger}', '{self.status}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20))
    points = db.Column(db.Integer, default = 0)
    avg_rating = db.Column(db.Integer, default= 5)
    cars = db.relationship('Car', back_populates='owner', lazy=True, cascade="all, delete")
    reviews = db.relationship('Review', back_populates='user', lazy=True, cascade="all, delete")
    journeys = db.relationship('Journeys_Users', back_populates='passenger', lazy='dynamic')
    journeys_driver = db.relationship('Journey', back_populates='driver', lazy=True)

    # What we return to the user
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.name}', {self.cars})"

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(20), nullable=False)
    maker = db.Column(db.String(20), nullable=False)
    reg_num = db.Column(db.String(8), nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    fuel = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', back_populates='cars', lazy=True)

    def __repr__(self):
        return f"Car('{self.model}', '{self.maker}', '{self.seats}')"

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(500))
    journey_id = db.Column(db.Integer, db.ForeignKey('journey.id'), nullable=False)
    rating = db.Column(db.Integer, default=5)
    user = db.relationship('User', back_populates='reviews', lazy=True)

    def __repr__(self):
        return f"Review('{self.journey_id}', '{self.user_id}','{self.rating}'"

class Journey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    driver = db.relationship('User', back_populates = 'journeys_driver', lazy=True)
    num_pass = db.Column(db.Integer, nullable=False)
    start_loc = db.Column(db.String, nullable=False)
    end_loc = db.Column(db.String, nullable=False)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    start_time = db.Column(db.String)
    end_time = db.Column(db.String)
    start_lat = db.Column(db.Float)
    start_long = db.Column(db.Float)
    end_lat = db.Column(db.Float)
    end_long = db.Column(db.Float)
    status = db.Column(db.String, default='Active')
    passengers = db.relationship('Journeys_Users', back_populates='journey', lazy='dynamic')

    def __repr__(self):
        return f"Journey('{self.driver_id}', '{self.num_pass}','{self.start_loc}', '{self.end_loc}'"


###### SCHEMAS TO JSONIFY DATA ######
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        
class CarSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Car
        include_fk = True
        include_relationship = True

class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review
        include_fk = True
        include_relationship = True
        
class JourneySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Journey
        include_fk = True
        include_relationship = True

class Journeys_UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Journeys_Users
        include_fk = True
        include_relationship = True