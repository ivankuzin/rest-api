from flask import Flask, jsonify, request
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

client = app.test_client()

engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

from models import *

Base.metadata.create_all(bind=engine)

# CRUD for dealers

@app.route('/dealers', methods=['GET'])
def get_dealers_list():
    '''Returns the list of dealers in JSON'''
    dealers = Dealer.query.all()
    serialized = []
    for dealer in dealers:
        serialized.append({
            'id': dealer.id,
            'name': dealer.name,
            'city': dealer.city
        })
    return jsonify(serialized)


@app.route('/dealers', methods=['POST'])
def update_dealers_list():
    '''Adding dealer to dealers list'''
    new_one = Dealer(**request.json)
    session.add(new_one)
    session.commit()
    serialized = {
        'id': new_one.id,
        'name': new_one.name,
        'city': new_one.city
    }
    return jsonify(serialized)


@app.route('/dealers/<int:dealer_id>', methods=['PUT'])
def update_dealer(dealer_id):
    '''Update data for a certain dealer'''
    item = Dealer.query.filter(Dealer.id == dealer_id).first()
    params = request.json
    if not item:
        return {'message': 'No dealer with this id'}, 400
    for key, value in params.items():
        setattr(item, key, value)
    session.commit()
    serialized = {
        'id': item.id,
        'name': item.name,
        'city': item.city
    }
    return serialized


@app.route('/dealers/<int:dealer_id>', methods=['DELETE'])
def delete_dealer(dealer_id):
    '''Delete certain dealer and it`s cars'''
    item = Dealer.query.filter(Dealer.id == dealer_id).first()
    if not item:
        return {'message': 'No dealer with this id'}, 400

    #Second step not needed, adding CASCADE
    '''cars = Car.query.filter(Car.dealer_id == dealer_id).all()
    for car in cars:    
        session.delete(car)'''

    session.delete(item)
    session.commit()
    return '', 204


# CRUD for cars

@app.route('/cars', methods=['GET'])
def get_cars_list():
    '''Returns the list of cars in JSON'''
    cars = Car.query.all()
    serialized = []
    for car in cars:
        serialized.append({
            'id': car.id,
            'brand': car.brand,
            'model': car.model,
            'vin' : car.vin,
            'dealer_id' : car.dealer_id
        })
    return jsonify(serialized)


@app.route('/cars', methods=['POST'])
def update_car_list():
    '''Adding car to cars list'''
    new_one = Car(**request.json)
    session.add(new_one)
    session.commit()
    serialized = {
        'id': new_one.id,
        'brand': new_one.brand,
        'model': new_one.model,
        'vin' : new_one.vin,
        'dealer_id' : new_one.dealer_id
    }
    return jsonify(serialized)


@app.route('/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    '''Update data for a certain car'''
    item = Car.query.filter(Car.id == car_id).first()
    params = request.json
    if not item:
        return {'message': 'No cars with this id'}, 400
    for key, value in params.items():
        setattr(item, key, value)
    session.commit()
    serialized = {
        'id': item.id,
        'brand': item.brand,
        'model': item.model,
        'vin' : item.vin,
        'dealer_id' : item.dealer_id
    }
    return serialized


@app.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    '''Delete certain car'''
    item = Car.query.filter(Car.id == car_id).first()
    if not item:
        return {'message': 'No cars with this id'}, 400
    session.delete(item)
    session.commit()
    return '', 204

# Some extra operations

@app.route('/cars/<string:brand>', methods=['GET'])
def get_brand(brand):
    '''Returns the list of specific car brand in JSON'''
    cars = Car.query.filter(Car.brand == brand).all()
    serialized = []
    for car in cars:
        serialized.append({
            'id': car.id,
            'brand': car.brand,
            'model': car.model,
            'vin' : car.vin,
            'dealer_id' : car.dealer_id
        })
    return jsonify(serialized)

@app.route('/cars/<string:brand>/<string:model>', methods=['GET'])
def get_model(brand,model):
    '''Returns the list of specific car brand and model in JSON'''
    cars = Car.query.filter((Car.model == model) and (Car.brand == brand)).all()
    serialized = []
    for car in cars:
        serialized.append({
            'id': car.id,
            'brand': car.brand,
            'model': car.model,
            'vin' : car.vin,
            'dealer_id' : car.dealer_id
        })
    return jsonify(serialized)

@app.route('/dealers/<int:dealer_id>', methods=['GET'])
def get_dealer(dealer_id):
    '''Returns the list of all cars of a certain dealer'''
    cars = Car.query.filter(Car.dealer_id == dealer_id).all()
    serialized = []
    for car in cars:
        serialized.append({
            'id': car.id,
            'brand': car.brand,
            'model': car.model,
            'vin' : car.vin, #Easter egg: car.vin.diesel (could be fun XD)
            'dealer_id' : car.dealer_id
        })
    return jsonify(serialized)



@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run(debug = 'True')
