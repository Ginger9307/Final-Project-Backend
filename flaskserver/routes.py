from flaskserver.models import Passenger, PassengerSchema, User, Car, Review, Journey, UserSchema, CarSchema, ReviewSchema, JourneySchema, PassengerSchema
from flaskserver import app, db, login_manager
from flask import request, jsonify, flash, render_template, redirect
from flask_bcrypt import Bcrypt
from flask_login import login_user, login_required, logout_user

#Login Helpers
bcrypt = Bcrypt()
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


#Load schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
car_schema = CarSchema()
cars_schema = CarSchema(many=True)
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)
journey_schema = JourneySchema()
journeys_schema = JourneySchema(many=True)
passenger_schema = PassengerSchema()
passengers_schema = PassengerSchema(many=True)

#Default route to check the server is up and running
@app.route('/')
def home():
    return 'Hello World!'

#Login Page 
@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        username = request.json['username']
        password = request.json['password']
        user = User.query.filter_by(username=username).first()
        if user:
            #verify password
            value = bcrypt.check_password_hash(user.password, password)
            if value:
                    login_user(user)
                    return jsonify({"Success": True})
            else:
                return jsonify({"Error": "Wrong Password"})
        else:
            return jsonify({"Error": "User not found"})
    except Exception as e:
        return jsonify({"Error": "Can't login"})

#Logout Page
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    try:
        logout_user()
        return  jsonify({"Success": "logout succesful"})
    except Exception as e:
        return jsonify({"Error": "Could not logout"})

#Create new User
@app.route('/register', methods=['POST'])
def register():
    try:
        name = request.json['name']
        username= request.json['username']
        email= request.json['email']
        password= request.json['password']

        #hash password
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(name = name, username = username, password=hashed_pw, email=email)
        db.session.add(new_user)
        db.session.commit()

        return user_schema.jsonify(new_user)
    except Exception as e:
        return jsonify({"Error": "Can't create user"})

#Get All Users
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    output = users_schema.dump(users)
    return jsonify(output)

#Get User by ID
@app.route('/users/<int:id>', methods=['GET'])
@login_required
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
    print(user_car)
    return jsonify(cars_schema.dump(user_car))

#Create Cars from User ID
@app.route('/users/<int:id>/cars', methods=['POST'])
def create_user_car(id):
    try:
        model = request.json['model']
        maker = request.json['maker']
        reg_num = request.json['reg_num']
        seats = request.json['seats']

        new_car = Car(model=model, maker=maker, reg_num=reg_num, seats=seats, user_id=id)
        db.session.add(new_car)
        db.session.commit()

        return car_schema.jsonify(new_car)
    except Exception as e:
        return jsonify({"Error": "Can't create car"})

#Get All Reviews
@app.route('/reviews', methods=['GET'])
def get_all_reviews():
    reviews = Review.query.all()
    return jsonify(reviews_schema.dump(reviews))

#Get Reviews from User ID
@app.route('/users/<int:id>/reviews', methods=['GET'])
def get_user_reviews(id):
    user_reviews = db.session.query(Review.id, Review.journey_id, Review.content, Review.rating, Review.user_id).join(User).filter(Review.user_id==id).all()
    print(user_reviews)
    return jsonify(reviews_schema.dump(user_reviews))

#Get a specific review from a user
@app.route('/users/<int:u_id>/reviews/<int:r_id>', methods=['GET'])
def get_review(u_id, r_id):
    review = db.session.query(Review.id, Review.journey_id, Review.content, Review.rating, Review.user_id).join(User).filter(Review.user_id==u_id).filter_by(id =r_id).first()
    print(review)
    return jsonify(review_schema.dump(review))

#Create a Review using User ID
@app.route('/users/<int:id>/reviews', methods=['POST'])
def create_user_review(id):
    try:
        journey_id = request.json['journey_id']
        content = request.json['content']
        rating = request.json['rating']
        
        new_review = Review(journey_id = journey_id, content=content, rating=rating, user_id = id)
        db.session.add(new_review)
        db.session.commit()
        print(new_review)
        return review_schema.jsonify(new_review)
    except Exception as e:
        return jsonify({"Error": "Can't create review"})

#Get All Journeys
@app.route('/journeys', methods=['GET'])
def get_journeys():
    journeys = Journey.query.all()
    return jsonify(journeys_schema.dump(journeys))

#Add a new Journey
@app.route('/journeys', methods=['POST'])
def create_journey():
    try:
        driver_id = request.json['driver_id']
        num_pass = request.json['num_pass']
        start_loc = request.json['start_loc']
        end_loc = request.json['end_loc']
        start_datetime = request.json['start_datetime']
        end_datetime = request.json['end_datetime']
        start_lat = request.json['start_lat']
        start_long = request.json['start_long']
        end_lat = request.json['end_lat']
        end_long = request.json['end_long']

        new_journey = Journey(driver_id = driver_id, num_pass=num_pass,start_loc=start_loc,
        end_loc=end_loc, start_datetime=start_datetime, end_datetime=end_datetime, start_lat=start_lat, end_lat=end_lat, start_long=start_long, end_long=end_long)
        db.session.add(new_journey)
        db.session.commit()

        return journey_schema.jsonify(new_journey)
    except Exception as e:
        return jsonify({"Error": "Can't create new journey"})

#Route to see the details of a particular journey
@app.route('/journeys/<int:journey_id>', methods=['GET'])
def journey_info(id):
    journey = db.session.query(Journey.id, Journey.driver_id, Journey.num_pass, Journey.start_datetime, Journey.end_datetime, Journey.start_lat, Journey.start_long, Journey.start_loc, Journey.end_lat, Journey.end_long, Journey.end_loc).join(User).filter(Journey.driver_id==id).all()
    return jsonify(journeys_schema.dump(journey))

#Route to see all passenger-journey relations
@app.route('/p-j-relations', methods=['GET'])
def passengers_journey():
    p_j = Passenger.query.all()
    return jsonify(passenger_schema.dump(p_j))

#############################################################################



#Route to accept/reject a passener entry
@app.route('/journeys/<int:journey_id>/passengers/<int:passenger_id>/status', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def journey_passengers_status():
    return "Here we should see and update the passengers' status in the journey (in or out of it)"

#Route to request access to journey 
@app.route('/journeys/<int:journey_id>/passengers/<int:passenger_id>/request', methods=['GET', 'POST', 'PATCH'])
def journey_passenger_request():
    return "Here we should see the request of users trying to get in (still WIP)"