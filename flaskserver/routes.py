from flaskserver.controllers import users
from flaskserver.models import User, Car, UserSchema
from flaskserver import app
from flask import request,jsonify

user_schema = UserSchema()
users_schema = UserSchema(many=True)

#Testing Routes for DB
@app.route('/test', methods=['GET'])
def get_all_users():
    users = User.query.all()
    output = users_schema.dump(users)
    print(output)
    return jsonify(output)

#Default route to check the server is up and running
@app.route('/')
def home():
    return 'Hello World!'

#Route to get all users and add new users
@app.route('/users', methods=['GET', 'POST'])
def all_users():
    fns = {
        'GET': users.showAll
    }
    resp, code = fns[request.method](request)
    return jsonify(resp), code

#Route for a particular user
@app.route('/users/<int:user_id>', methods=['GET', 'PATCH'])
def user_methods(user_id):
    fns = {
        'GET': users.showOne
    }
    resp, code = fns[request.method](request, user_id)
    return jsonify(resp), code

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