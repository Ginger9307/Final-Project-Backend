from datetime import datetime
from flaskserver import db, ma
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    username = StringField('Enter your username', validators=[DataRequired()])
    name = StringField('Enter your name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('submit')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20))
    points = db.Column(db.Integer, default = 0)
    avg_rating = db.Column(db.Integer, default= 0)
    car = db.relationship('Car', backref='owner', lazy=True)
    
    # What we return to the user
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.name}', {self.car})"

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(20), nullable=False)
    maker = db.Column(db.String(20), nullable=False)
    reg_num = db.Column(db.String(8), nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Car('{self.model}', '{self.maker}', '{self.seats}')"

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(500))
    journey_id = db.Column(db.Integer, db.ForeignKey('journey.id'), nullable=False)
    rating = db.Column(db.Integer, default=5)

    def __repr__(self):
        return f"Review('{self.journey_id}', '{self.user_id}','{self.rating}'"

class Journey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    num_pass = db.Column(db.Integer, nullable=False)
    start_loc = db.Column(db.String, nullable=False)
    end_loc = db.Column(db.String, nullable=False)
    start_datetime = db.Column(db.String, nullable=False, default = datetime.utcnow)
    end_datetime = db.Column(db.String)
    start_lat = db.Column(db.Float)
    start_long = db.Column(db.Float)
    end_lat = db.Column(db.Float)
    end_long = db.Column(db.Float)
    status = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"Journey('{self.driver_id}', '{self.num_pass}','{self.start_loc}', '{self.end_loc}', '{self.start_datetime}'"

class Passenger(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    journey_id = db.Column(db.Integer, db.ForeignKey('journey.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    req_status = db.Column(db.Boolean, default = True, nullable=False)

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

class PassengerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Passenger
        include_fk = True
        include_relationship = True