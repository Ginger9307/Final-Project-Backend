#Dummy data for now
from werkzeug.exceptions import BadRequest

users = [
    {'id':1, 'name':'Tatiana', 'reviews': [
        {'id': 1, 'review': 'This was a pleasant trip'},
        {'id': 2, 'review': 'This was not pleasant trip'},
        {'id': 3, 'review': 'This was wonderful'}
        ]
    },
    {'id':2, 'name':'Pete', 'reviews': [
        {'id': 1, 'review': 'Wonderful views'},
        {'id': 2, 'review': 'Nice ride'},
        {'id': 3, 'review': 'Space was lacking'}
        ]},
    {'id':3, 'name':'Franklyn', 'reviews': [
        {'id': 1, 'review': 'This was a pleasant trip'},
        {'id': 2, 'review': 'Music was on point'}
        ]},
    {'id':4, 'name':'Amir', 'reviews': [
        {'id': 1, 'review': 'Driver arrived a bit late, but he made it up by getting to our destination earlier'},
        {'id': 2, 'review': 'Nice car and seats,v ery clean'},
        ]},
    {'id':5, 'name':'Eddie', 'reviews': [
        {'id': 1, 'review': 'Quick and cozy ride'}
        ]},
]

def showAll(req):
    return [u for u in users], 200

def showOne(req, id):
    return find_by_id(id), 200

def reviews(req, id):
    return get_reviews(id), 200

#Helpers
def find_by_id(id):
    try:
        return next(user for user in users if user['id'] == id)
    except:
        raise BadRequest(f'Could not find user with id {id}')

def get_reviews(id):
    user = find_by_id(id)
    review_list = user['reviews']
    return review_list
    