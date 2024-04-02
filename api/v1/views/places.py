# api/v1/views/places.py
#!/usr/bin/python3
"""
    API for Place objects
"""

from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = City.get(city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places()]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = Place.get(place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = Place.get(place_id)
    if not place:
        abort(404)
    place.delete()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = City.get(city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')
    user_id = data['user_id']
    if not User.get(user_id):
        abort(404)
    new_place = Place(city_id=city_id, **data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = Place.get(place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Searches for places based on given criteria"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])
    
    if not states and not cities:
        places = Place.all()
    else:
        places = []
        for state_id in states:
            state = State.get(state_id)
            if state:
                for city in state.cities:
                    if city not in places:
                        places.extend(city.places)
        for city_id in cities:
            city = City.get(city_id)
            if city and city not in places:
                places.extend(city.places)

    if amenities:
        filtered_places = []
        for place in places:
            place_amenities = [amenity.id for amenity in place.amenities]
            if all(amenity_id in place_amenities for amenity_id in amenities):
                filtered_places.append(place)
        places = filtered_places

    return jsonify([place.to_dict() for place in places])