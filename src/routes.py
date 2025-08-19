from flask import Blueprint, jsonify
from models import db, User, Character, Vehicle, Planet

api_bp = Blueprint("api", __name__)


# Characters

@api_bp.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()

    if not characters:
        return jsonify({'msg': 'Character not found'}), 404
    
    return jsonify([char.serialize() for char in characters])


@api_bp.route('/characters/<int:character_id>', methods=['GET'])
def get_char_id(character_id):
    character = Character.query.get(character_id)

    if not character:
        return jsonify({'msg': 'Character not found'}), 404

    return jsonify(character.serialize())


@api_bp.route('/users/<int:user_id>/favorites/character/<int:char_id>', methods=['DELETE'])
def delete_char(user_id, char_id):
    user = db.session.get(User, user_id)
    character_dlt = Character.query.get(char_id)

    if not user or not character_dlt:
        return jsonify({'msg': 'User not found'}), 404
    
    if character_dlt in user.characters:
        user.characters.remove(character_dlt)
        db.session.commit()
    
    return jsonify(user.serialize()), 200



# Vehicles

@api_bp.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([veh.serialize() for veh in vehicles])

@api_bp.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle_id(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)

    if not vehicle:
        return jsonify({'msg': 'Vehicle not found'}), 404

    return jsonify(vehicle.serialize())


@api_bp.route('/users/<int:user_id>/favorite/vehicles/<int:vehicle_id>', methods=['POST'])
def add_vehicle(user_id, vehicle_id):
    user = db.session.get(User, user_id)
    vehicle = Vehicle.query.get(vehicle_id)

    if not user:
        return jsonify({'msg': 'User not found'}), 404
    
    if not vehicle:
        return jsonify({'msg': 'Vehicle not found'}), 404
    
    user.vehicles.append(vehicle)
    db.session.commit()
    return jsonify(user.serialize())

@api_bp.route('/users/<int:user_id>/favorites/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_fav_vehicle(user_id, vehicle_id):
    user = db.session.get(User, user_id)
    vehicle_delete = Vehicle.query.get(vehicle_id)

    if not user or not vehicle_delete:
        return jsonify({'msg': 'Vehicle not found'}), 404
    
    if vehicle_delete in user.vehicles:
        user.vehicles.remove(vehicle_delete)
        db.session.commit()
    
    return jsonify(user.serialize()), 200


# Users

@api_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users]), 200


@api_bp.route('/users/<int:user_id>/favorites', methods=['GET'])
def show_favorites(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({'msg': 'User not found'}), 404
    
    favorites_total = {
        'characters': [c.serialize() for c in user.characters],
        'vehicles': [v.serialize() for v in user.vehicles],
        'planets': [p.serialize() for p in user.planets],
    }
    return jsonify(favorites_total), 200


@api_bp.route('/users/<int:user_id>/favorite/characters/<int:char_id>', methods=['POST'])
def add_favorite(user_id, char_id):
    user = db.session.get(User, user_id)
    character = Character.query.get(char_id)

    if not user:
        return jsonify({'msg': 'User not found'}), 404
    
    if not character:
        return jsonify({'msg': 'Character not found'}), 404

    user.characters.append(character)
    db.session.commit()
    return jsonify(user.serialize())


# Planets

@api_bp.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([pl.serialize() for pl in planets])

@api_bp.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_id(planet_id):
    planet = Planet.query.get(planet_id)

    if not planet:
        return jsonify({'msg': 'Planet not found'}), 404

    return jsonify(planet.serialize())


@api_bp.route('/users/<int:user_id>/favorite/planets/<int:planet_id>', methods=['POST'])
def add_planet(user_id, planet_id):
    user = db.session.get(User, user_id)
    planet = Planet.query.get(planet_id)

    if not user:
        return jsonify({'msg': 'User not found'}), 404
    
    if not planet:
        return jsonify({'msg': 'Planet not found'}), 404
    
    user.planets.append(planet)
    db.session.commit()
    return jsonify(user.serialize())

@api_bp.route('/users/<int:user_id>/favorites/planets/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(user_id, planet_id):
    user = db.session.get(User, user_id)
    planet_delete = Planet.query.get(planet_id)

    if not user or not planet_delete:
        return jsonify({'msg': 'Planet not found'}), 404
    
    if planet_delete in user.planets:
        user.planets.remove(planet_delete)
        db.session.commit()
    
    return jsonify(user.serialize()), 200
