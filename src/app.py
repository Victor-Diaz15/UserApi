from flask import Flask, Response, jsonify, request
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/FlaskCrudDb'
mongo = PyMongo(app)

#Rutas
#Ruta post
@app.route('/users', methods = ['POST'])
def CreateUser():
    #receiving data
    username = request.json['username'] #Victor
    password = request.json['password'] #20210834
    email = request.json['email'] #vic@gmail.com

    if username and password and email:
        hashed_password = generate_password_hash(password)
        id = mongo.db.users.insert_one(
            {
                'username': username, 
                'email': email,
                'password': hashed_password
            }
        )
        response = jsonify({
            'id': str(id.inserted_id),
            'username': username, 
            'email': email,
            'password': hashed_password
        })
        response.status_code = 201
        return response
    else:
        return not_found()

#Ruta Get
@app.route('/users', methods = ['GET'])
def GetUsers():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype= 'application/json')

#Ruta GetUser
@app.route('/users/<id>', methods = ['GET'])
def GetUser(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id) })
    response = json_util.dumps(user)
    return Response(response, mimetype='application/json')

#Ruta para Eliminar un user
@app.route('/users/<id>', methods = ['DELETE'])
def DeleteUser(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User with ' + id + ' was deleted succesfully'})
    return response

#Ruta para editar un user
@app.route('/users/<id>', methods = ['PUT'])
def UpdateUser(id):
    username = request.json['username'] #Victor
    password = request.json['password'] #20210834
    email = request.json['email'] #vic@gmail.com

    if username and password and email:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': {
            'username': username, 
            'email': email,
            'password': hashed_password
        }})
        response = jsonify({'message': 'User with ' + id + 'was Updated succesfully'})
        response.status_code = 200
        return response
    else:
        return not_found()

#error handler, not Found user
@app.errorhandler(404)
def not_found(error = None):
    response = jsonify({
        'message': 'Resource Not Found: ' + request.url,
        'status': 404
    }) 
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug = True)