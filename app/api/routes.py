from flask import Blueprint, request, jsonify, render_template, json
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema
from flask_login import current_user

api = Blueprint('api', __name__, url_prefix = '/api', template_folder= 'api_templates')

@api.route('/cars', methods= ['POST'])
@token_required
def create_car(current_token):
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    color = request.json['color']
    user_token = current_token.token

    print(f'BIG TESTER: {current_token.token}')

    car = Car(make, model, year, user_token, color)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

# retrieve all the cars
@api.route('/displaycars')
def display():

    return render_template('display.html', title ='Your Cars', cars = current_user.cars)

    user = current_token.token
    cars = Car.query.filter_by(user_token = user).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

#display all cars
@api.route('/cars', methods= ['GET'])
@token_required
def display_cars(current_token):
    user = current_token.token
    cars = Car.query.filter_by(user_token = user).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

# display a single car
@api.route('/car/<id>', methods= ['GET'])
@token_required
def get_single_car(current_token, id):
    car = Car.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)


#update a particular car
@api.route('cars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_token, id):
   car = Car.query.get(id)
   car.make = request.json['make']
   car.model = request.json['model']
   car.year = request.json['year']
   car.color= request.json['color']
   car.user_token = current_token.token

   db.session.commit()
   response = car_schema.dump(car)
   return jsonify(response)

@api.route('/car/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)