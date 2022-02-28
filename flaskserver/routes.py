from flaskserver.controllers import users
from flaskserver.models import User, Car, UserSchema, CarSchema, RegisterForm
from flaskserver import app, db
from flask import request, jsonify, flash, render_template
from werkzeug.security import generate_password_hash


user_schema = UserSchema()
users_schema = UserSchema(many=True)
car_schema = CarSchema()
cars_schema = CarSchema(many=True)

#Default route to check the server is up and running
@app.route('/')
def home():
    return 'Hello World!'

#Get All Users
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    output = users_schema.dump(users)
    return jsonify(output)

#Get User by ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.filter_by(id = id).first()
    output = user_schema.dump(user)
    return jsonify(output)

#Get All Cars
@app.route('/cars', methods=['GET'])
def get_all_cars():
    cars = Car.query.all()
    output = cars_schema.dump(cars)
    return jsonify(output)

#Get Cars from User ID
@app.route('/users/<int:id>/cars', methods=['GET'])
def get_user_car(id):
    user_car = db.session.query(Car.id, Car.maker, Car.model, Car.reg_num, Car.seats, Car.user_id).join(User).filter(Car.user_id==id).all()
    return jsonify(cars_schema.dump(user_car))

#Register
@app.route('/register', methods=['GET','POST'])
def sign_up():
    name =''
    form = RegisterForm()
    # Validate Form, if email does not exist add to database
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            # hash password
            hashed_pw = generate_password_hash(form.password_hash.data, 'sha256')
            user = User(username=form.username.data, name=form.name.data, email=form.email.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data 
        # clear form
        form.name.data = ''   
        form.email.data = ''
        form.password_hash.data = ''
        # flash message
        flash('User Added!')
    # return all users by id 
    our_users = User.query.order_by(User.id)
    return render_template('/register.html', name = name, form = form, our_users=our_users) 

#############################################################################

#Route too see the review of the users
@app.route('/users/<int:user_id>/reviews', methods=['GET', 'POST'])
def user_reviews(user_id):
    fns = {
        'GET': users.reviews
    }
    resp, code = fns[request.method](request, user_id)
    return jsonify(resp), code

#Route to see car registered by the users
@app.route('/users/<int:user_id>/car', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def user_car():
    return 'Here we will see the cars registered by the users'

#Route to see all journeys
@app.route('/journeys', methods=['GET', 'POST', 'PATCH'])
def all_journeys():
    return 'Here we will see a list of journeys and their details'

#Route to see the details of a particular journey
@app.route('/journeys/<int:journey_id>', methods=['GET'])
def journey_info():
    return 'Here we will see the details of a specific journey'

#Route to see all passengers wanting to join a journey
@app.route('/journeys/<int:journey_id>/passengers', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def journey_passengers():
    return 'Here we will see a list of passengers for a particular journey'

#Route to accept/reject a passener entry
@app.route('/journeys/<int:journey_id>/passengers/<int:passenger_id>/status', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def journey_passengers_status():
    return "Here we should see and update the passengers' status in the journey (in or out of it)"

#Route to request access to journey 
@app.route('/journeys/<int:journey_id>/passengers/<int:passenger_id>/request', methods=['GET', 'POST', 'PATCH'])
def journey_passenger_request():
    return "Here we should see the request of users trying to get in (still WIP)"