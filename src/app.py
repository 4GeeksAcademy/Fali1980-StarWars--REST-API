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
from models import db, User, Character, Planet, Favorites_characters, Favorites_planets
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


# INICIO DE CÓDIGO-------------------------------

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# TODOS LOS GET

@app.route('/user', methods=['GET'])
def handle_hello():
    all_users = User.query.all()
    print(all_users)
    results = list(map(lambda user: user.serialize(), all_users))
    print(results)

    response_body = {
        "msg": "LEER LOS USUARIOS "
    }

    return jsonify(results), 200



@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    return jsonify(user.serialize()), 200



@app.route('/user/favorites', methods=['GET'])
def get_favorites():
    received_user_id = request.json.get('id')
    results = Favorites_characters.query.filter_by(user_id = received_user_id).all()
    character_favorites_serialized = list(map(lambda element: element.serialize(), results))
    results_2 = Favorites_planets.query.filter_by(user_id = received_user_id).all()
    planets_favorites_serialized = list(map(lambda element: element.serialize(), results_2))

    return jsonify({'planets_favorites': planets_favorites_serialized,'character_favorites': character_favorites_serialized}), 200



@app.route('/character', methods=['GET'])
def get_characters():
    all_characters = Character.query.all()
    print(all_characters)
    results = list(map(lambda character: character.serialize(), all_characters))
    print(results)

    response_body = {
        "msg": "LEER LOS CHARACTERS "
    }

    return jsonify(results), 200



@app.route('/character/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.filter_by(id=character_id).first()
    return jsonify(character.serialize()), 200



@app.route('/planet', methods=['GET'])
def get_planets():
    all_planets = Planet.query.all()
    print(all_planets)
    results = list(map(lambda planet: planet.serialize(), all_planets))
    print(results)

    response_body = {
        "msg": "LEER LOS PLANETS "
    }

    return jsonify(results), 200



@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.filter_by(id=planet_id).first()
    return jsonify(planet.serialize()), 200



# TODOS LOS POST

@app.route('/character', methods=['POST'])
def create_character():
    # Leer los datos que envia solicitud (body)
    data = request.json
    if not "name" in data:
        return jsonify("Se debe enviar el character"), 400
    if data["name"] == "":
        return jsonify("El character no debe ser vacio"), 400
    # Crear character nuevo
    charact = Character(**data)
    db.session.add(charact)
    db.session.commit()

    response_body = {
        "msg": "CREAR LOS USUARIOS "
    }

    return jsonify(response_body), 200



@app.route('/planet', methods=['POST'])
def create_planet():
    # Leer los datos que envia solicitud (body)
    data = request.json
    if not "diameter" in data:
        return jsonify("Se debe enviar el planet"), 400
    if data["diameter"] == "":
        return jsonify("El planet no debe ser vacio"), 400
    # Crear planet nuevo
    plane = Planet(**data)
    db.session.add(plane)
    db.session.commit()

    response_body = {
        "msg": "CREAR LOS PLANETAS "
    }

    return jsonify(response_body), 200



@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_fav_planet(planet_id):
            user_id = request.json.get('user_id')
            existing_favorite = Favorites_planets.query.filter_by(user_id=user_id, planet_id=planet_id).first()            
            if existing_favorite:
                return jsonify({"msg": "Personaje favorio del usuario"}), 400            
            planet = Planet.query.get(planet_id)
            if not planet:
                return jsonify({"msg": "Planeta no existe"}), 404 
            # Crear nuevo planeta favorito          
            new_favorite = Favorites_planets(user_id=user_id, planet_id=planet_id)
            db.session.add(new_favorite)
            db.session.commit()
            return jsonify({"msg": "Planeta establecido como favorito"}), 200



@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_fav_character(character_id):
    user_id = request.json.get('user_id')
    
    existing_favorite = Favorites_characters.query.filter_by(user_id=user_id, character_id=character_id).first()
    if existing_favorite:
        return jsonify({"msg": "Personaje favorito del usuario"}), 400
    
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"msg": "Personaje no existe"}), 404
    # Crear nuevo personaje favorito  
    new_favorite = Favorites_characters(user_id=user_id, character_id=character_id)
    db.session.add(new_favorite)
    db.session.commit()
    
    return jsonify({"msg": "Personaje establecido como favorito"}), 200




# TODOS LOS DELETE

@app.route('/character/<int:id>', methods=['DELETE'])
def delete_character(id):
    # Buscar el personaje por su ID en la base de datos
    character = Character.query.get(id)

    # Si no se encuentra el personaje, devuelve un error 404
    if character is None:
        return jsonify("Personaje no encontrado"), 404

    # Eliminar el personaje de la base de datos
    db.session.delete(character)
    db.session.commit()

    # Devolver una respuesta exitosa
    return jsonify({"msg": "Personaje eliminado exitosamente"}), 200



@app.route('/planet/<int:id>', methods=['DELETE'])
def delete_planet(id):
    # Buscar el personaje por su ID en la base de datos
    planet = Planet.query.get(id)

    # Si no se encuentra el personaje, devuelve un error 404
    if planet is None:
        return jsonify("Planeta no encontrado"), 404

    # Eliminar el personaje de la base de datos
    db.session.delete(planet)
    db.session.commit()

    # Devolver una respuesta exitosa
    return jsonify({"msg": "Personaje eliminado exitosamente"}), 200



@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_one_fav_planet(planet_id):

    # user_id = request.json.get('user_id')  # Obtener user_id del cuerpo de la solicitud
    # print (planet_id, user_id)
    # return jsonify({"msg": "Fav Planet deleted successfully"}), 200
    
        user_id = request.json.get('user_id')  # Obtener user_id del cuerpo de la solicitud
        print (planet_id, user_id)
        existing_favorite = Favorites_planets.query.filter_by(user_id=user_id, planet_id=planet_id).first()
        if existing_favorite:
            db.session.delete(existing_favorite)  # Eliminar la fila existente
            db.session.commit()
            return jsonify({"msg": "Planeta favorito borrado"}), 200
        planet = Planet.query.get(planet_id)
        if not planet:
            return jsonify({"msg": "planeta favorito no existe"}), 404
        

        
@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_one_fav_character(character_id):
    user_id = request.json.get('user_id')  # Obtener user_id del cuerpo de la solicitud
    existing_favorite = Favorites_characters.query.filter_by(user_id=user_id, character_id=character_id).first()
    
    if existing_favorite:
        db.session.delete(existing_favorite)  # Eliminar la fila existente
        db.session.commit()
        return jsonify({"msg": "Personaje favorito borrado"}), 200
    
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"msg": "Personaje favorito no existe"}), 404



# FIN DE CÓDIGO-----------------------------------

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
