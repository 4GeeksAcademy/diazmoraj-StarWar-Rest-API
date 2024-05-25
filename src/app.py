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
from models import db, User
from models import db, Planet
from models import db, People
from models import db, Starship
from models import db, FavPlanet
from models import db, FavPeople
from models import db, FavStarship
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

# Rutas para obtener usuarios 
@app.route('/user', methods=['GET'])
def get_all_user():
    all_users = User.query.all()
    users_serialized = []
    for user in all_users:
        users_serialized.append(user.serialize())
    print(users_serialized)
    return jsonify({"data": "all_user"}), 200

# Rutas para obtener usuarios por ID
@app.route("/user/<int:id>", methods=['GET'])
def get_single_user(id):
    single_user = User.query.get(id)
    if single_user is None:
        return jsonify({"msg": "El usuario con el ID: {} no existe".format(id)}), 400
    return jsonify({"data": single_user.serialize()}), 200

# Rutas para crear usuarios
@app.route('/user', methods=["POST"])
def new_user():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": "Debes enviar informacion en el body"}), 400
    if "name" not in body:
        return jsonify({"msg": "El campo nombre es obligatorio"}), 400
    if "email" not in body:
        return jsonify({"msg": "El campo email es obligatorio"}), 400
    if "password" not in body:
        return jsonify({"msg": "El campo password es obligatorio"}), 400
    
    new_user = User()
    new_user.name = body["name"]
    new_user.email = body["email"]
    new_user.password = body["password"]
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "OK"}), 200

#Rutas para borrar usuarios
@app.route("/user/<int:id>", methods=["DELETE"])
def delete_user(id):
    try:
        delete_user = User.query.get(id)
        db.session.delete(delete_user)
        db.session.commit()
        return jsonify({"msg": "OK"}), 204
    except Exception as error:
        db.session.rollback()
        return jsonify({"msg": error.args[0]}), 500
    
    # Rutas para obtener usuarios 

# Rutas para obtener planetas
@app.route('/planet', methods=['GET'])
def get_all_planet():
    all_planets = Planet.query.all()
    planets_serialized = []
    for planet in all_planets:
        planets_serialized.append(planet.serialize())
    print(planets_serialized)
    return jsonify({"data": "all_planet"}), 200

# Rutas para obtener planetas por ID
@app.route("/planet/<int:id>", methods=['GET'])
def get_single_planet(id):
    single_planet = Planet.query.get(id)
    if single_planet is None:
        return jsonify({"msg": "El planeta con el ID: {} no existe".format(id)}), 400
    return jsonify({"data": single_planet.serialize()}), 200

# Rutas para crear planetas
@app.route('/planet', methods=["POST"])
def new_planet():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": "Debes enviar informacion en el body"}), 400
    if "name" not in body:
        return jsonify({"msg": "El campo nombre es obligatorio"}), 400
    if "climate" not in body:
        return jsonify({"msg": "El campo climate es obligatorio"}), 400
    if "populatiom" not in body:
        return jsonify({"msg": "El campo population es obligatorio"}), 400
    if "gravity" not in body:
        return jsonify({"msg": "El campo gravity es obligatorio"}), 400
    
    new_planet = Planet()
    new_planet.name = body["name"]
    new_planet.climate = body["climate"]
    new_planet.population = body["population"]
    new_planet.gravity = body["gravity"]
    db.session.add(new_planet)
    db.session.commit()

    return jsonify({"msg": "OK"}), 200

#Rutas para borrar planetas
@app.route("/planet/<int:id>", methods=["DELETE"])
def delete_planet(id):
    try:
        delete_planet = Planet.query.get(id)
        db.session.delete(delete_planet)
        db.session.commit()
        return jsonify({"msg": "OK"}), 204
    except Exception as error:
        db.session.rollback()
        return jsonify({"msg": error.args[0]}), 500

# Rutas para obtener personas
@app.route('/people', methods=['GET'])
def get_all_poeple():
    all_people = People.query.all()
    people_serialized = []
    for people in all_people:
        people_serialized.append(people.serialize())
    print(people_serialized)
    return jsonify({"data": "all_people"}), 200

# Rutas para obtener personas por ID
@app.route("/people/<int:id>", methods=['GET'])
def get_single_peoplet(id):
    single_people = People.query.get(id)
    if single_people is None:
        return jsonify({"msg": "La persona con el ID: {} no existe".format(id)}), 400
    return jsonify({"data": single_people.serialize()}), 200

# Rutas para crear personas
@app.route('/people', methods=["POST"])
def new_people():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": "Debes enviar informacion en el body"}), 400
    if "name" not in body:
        return jsonify({"msg": "El campo nombre es obligatorio"}), 400
    if "gender" not in body:
        return jsonify({"msg": "El campo gender es obligatorio"}), 400
    if "height" not in body:
        return jsonify({"msg": "El campo height es obligatorio"}), 400
    if "mass" not in body:
        return jsonify({"msg": "El campo mass es obligatorio"}), 400
    
    new_people = People()
    new_people.name = body["name"]
    new_people.gender = body["gender"]
    new_people.height = body["height"]
    new_people.mass = body["mass"]
    db.session.add(new_people)
    db.session.commit()

    return jsonify({"msg": "OK"}), 200

#Rutas para borrar personas
@app.route("/people/<int:id>", methods=["DELETE"])
def delete_people(id):
    try:
        delete_people = People.query.get(id)
        db.session.delete(delete_people)
        db.session.commit()
        return jsonify({"msg": "OK"}), 204
    except Exception as error:
        db.session.rollback()
        return jsonify({"msg": error.args[0]}), 500
    
# Rutas para obtener naves
@app.route('/starships', methods=['GET'])
def get_all_starship():
    all_starship = Starship.query.all()
    starships_serialized = []
    for starship in all_starship:
        starships_serialized.append(starship.serialize())
    print(starships_serialized)
    return jsonify({"data": "all_starship"}), 200

# Rutas para obtener naves por ID
@app.route("/starship/<int:id>", methods=['GET'])
def get_single_starship(id):
    single_starship = Starship.query.get(id)
    if single_starship is None:
        return jsonify({"msg": "La nave con el ID: {} no existe".format(id)}), 400
    return jsonify({"data": single_starship.serialize()}), 200

# Rutas para crear naves
@app.route('/starship', methods=["POST"])
def new_starship():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": "Debes enviar informacion en el body"}), 400
    if "name" not in body:
        return jsonify({"msg": "El campo nombre es obligatorio"}), 400
    if "model" not in body:
        return jsonify({"msg": "El campo model es obligatorio"}), 400
    if "cost" not in body:
        return jsonify({"msg": "El campo cost es obligatorio"}), 400
    if "pilot" not in body:
        return jsonify({"msg": "El campo pilot es obligatorio"}), 400
    
    new_starship = Starship()
    new_starship.name = body["name"]
    new_starship.model = body["model"]
    new_starship.cost = body["cost"]
    new_starship.pilot = body["pilot"]
    db.session.add(new_starship)
    db.session.commit()

    return jsonify({"msg": "OK"}), 200

#Rutas para borrar naves
@app.route("/starship/<int:id>", methods=["DELETE"])
def delete_starship(id):
    try:
        delete_starship = Starship.query.get(id)
        db.session.delete(delete_starship)
        db.session.commit()
        return jsonify({"msg": "OK"}), 204
    except Exception as error:
        db.session.rollback()
        return jsonify({"msg": error.args[0]}), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
