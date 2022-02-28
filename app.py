from flask import Flask, render_template, flash
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
CORS(app)

# Create form Class
class RegisterForm(FlaskForm):
    name = StringField('Enter your name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('submit')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carpool.db'

#Initialise the database
db = SQLAlchemy(app)

#Create db models
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    points = db.Column(db.Integer)
    avg_rating = db.Column(db.Integer)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)    

    # function to return user
    def __repr__(self):
        return '<User %r>' % self.id






@app.route('/')
def home():
    return 'Hello World!'

@app.route('/register', methods=['GET', 'POST'])
def sign_up():
    name = None
    form = RegisterForm()
    # Validate Form, if email does not exist add to database
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data 
        # clear form
        form.name.data = ''   
        form.email.data = ''
        # flash message
        flash('User Added!')
    # return all users by id 
    our_users = Users.query.order_by(Users.id)       
    return render_template('register.html', name = name, form = form, our_users=our_users)