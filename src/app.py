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
def handle_hello():
    all_users = User.query.all()
    users_serialized = []
    for user in all_users:
        users_serialized.append(user.serialize())
    print(users_serialized)
    return jsonify({"data": "all_user"}), 200

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
    if "email" not in body:
        return jsonify({"msg": "El campo email es obligatorio"}), 400
    if "password" not in body:
        return jsonify({"msg": "El campo password es obligatorio"}), 400
    
    new_user = User()
    new_user.email = body["email"]
    new_user.password = body["password"]
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "OK"}), 200

@app.route("/user/<int:id>", methods=["DELETE"])
def delete_user(id):
    delete_user = User.query.get(id)
    db.session.delete(delete_user)
    db.session.commit()
    return jsonify({"msg": "OK"}), 200

#try: 
    db.session.rollback
#Exception


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
