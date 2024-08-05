"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,People,Planet,Favorite

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False


db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)




# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)







@app.route('/people', methods=['GET'])
def get_people():

    lista = People.query.all()
    lista = list(map(lambda x : x.serialize(), lista))

    response_body = {
        "result": lista 
    }
    
    return jsonify(response_body), 200

    

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    
    people = People.query.get_or_404(people_id)  # This will return a 404 if the person is not found
    return jsonify(people.serialize()), 200   


@app.route('/user', methods=['GET'])
def get_user():

     lista = User.query.all()
     lista = list(map(lambda x : x.serialize(), lista))
     
     response_body = {
        "result": lista 
    }
     
     return jsonify(response_body), 200






@app.route('/favorites', methods=['GET'])
def get_favorites():
    # Query all favorites from the database
    lista = Favorite.query.all()
    lista = list(map(lambda x : x.serialize(), lista))
   
    response_body = {
        "result": lista 
    }
    return jsonify(response_body), 200


@app.route('/planet', methods=['GET'])
def get_planets():

    lista = Planet.query.all()
    lista = list(map(lambda x : x.serialize(), lista))

    response_body = {
        "result": lista 
    }
    
    return jsonify(response_body), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    
    planet = Planet.query.get_or_404(planet_id)  # This will return a 404 if the person is not found
    return jsonify(planet.serialize()), 200   

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite(planet_id):
    
    user_id = User.query.get(1)
   
    if user_id is None:
        return jsonify({'error': 'User not logged in'}), 403
    
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({'error': 'Planet not found'}), 404
    
    existing_favorite = Favorite.query.filter_by(user_id=1, planet_id=planet_id).first()
    if existing_favorite:
        return jsonify({'message': 'Planet already in favorites'}), 200
    else:
        fav = Favorite()
        fav.user_id = 1
        fav.planet_id = planet_id

        db.session.add(fav)
        db.session.commit()
        return jsonify(fav.serialize()), 200
    

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    
    user_id = User.query.get(1)
   
    if user_id is None:
        return jsonify({'error': 'User not logged in'}), 403
    
    people = People.query.get(people_id)
    if people is None:
        return jsonify({'error': 'People not found'}), 404
    
    existing_favorite = Favorite.query.filter_by(user_id=1, people_id=people_id).first()
    if existing_favorite:
        return jsonify({'message': 'Planet already in favorites'}), 200
    else:
        fav = Favorite()
        fav.user_id = 1
        fav.people_id = people_id

        db.session.add(fav)
        db.session.commit()
        return jsonify(fav.serialize()), 200
    
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    # Assume user_id is retrieved from session or another authentication method
    user_id = 1  # This should be dynamically retrieved, e.g., from the session

    # Ensure user is logged in
    if user_id is None:
        return jsonify({'error': 'User not logged in'}), 403

    # Locate the favorite record
    favorite = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()

    if favorite is None:
        return jsonify({'error': 'Favorite not found'}), 404

    # Delete the favorite record
    db.session.delete(favorite)
    db.session.commit()

    return jsonify({'message': 'Favorite people removed successfully'}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    # Assume user_id is retrieved from session or another authentication method
    user_id = 1  # This should be dynamically retrieved, e.g., from the session

    # Ensure user is logged in
    if user_id is None:
        return jsonify({'error': 'User not logged in'}), 403

    # Locate the favorite record
    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()

    if favorite is None:
        return jsonify({'error': 'Favorite not found'}), 404

    # Delete the favorite record
    db.session.delete(favorite)
    db.session.commit()

    return jsonify({'message': 'Favorite planet removed successfully'}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
