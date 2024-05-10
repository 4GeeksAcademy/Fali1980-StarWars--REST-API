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
from models import db, User, Character, Planet
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


@app.route('/character', methods=['POST'])
def create_character():
    # Leer los datos que envia solicitud (body)
    data = request.json
    print(data)
    if not "name" in data:
        return jsonify("debes enviar el character"), 400
    if data["name"] == "":
        return jsonify("el character no debe ser vacio"), 400
    print(data.get("name"))
    print(data["name"])
    # Crear character nuevo
    charact = Character(**data)
    db.session.add(charact)
    db.session.commit()

    response_body = {
        "msg": "CREAR LOS USUARIOS "
    }

    return jsonify(response_body), 200

# FIN DE CÓDIGO-----------------------------------

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
