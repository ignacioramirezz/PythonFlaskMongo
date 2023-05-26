from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId

# import un string y crifrar y el otro es para chequear la contraseña

app = Flask(__name__)

#informacion para la conexion con la base de datos
app.config['MONGO_URI']='mongodb://localhost:27017/pythonmongodb'

mongo=PyMongo(app)

@app.route('/users',methods=['POST'])
def create_user():
    username = request.json['username'] # usuario_nuevo
    password = request.json['password'] #quiero cifrar esto
    email = request.json['email']
    if username and email and password:
        hashed_password = generate_password_hash(password)
        id = mongo.db.users.insert_one(
            {'username':username, 'email': email, 'password':hashed_password}
            # voy a devolver que el id (funciona asi mongo NOSQL) mas x datos fue creado
        )
        response = {
            'id': str(id),  ## convierte a un string el id
            'username': username,
            'password': hashed_password,
            'email' : email
        }
        return response
    else:
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resource Not Found' + request.url,
        'status' : 404 
    })
    response.status = 404
    return response


@app.route('/users',methods=['GET'])
def devolver_usuarios():
    my_users = mongo.db.users.find()
    ## quiero devolver devolver una lista de la forma json
    ## porque mongodb devuelve un bson que es el formato por defecto q guarda
    response =json_util.dumps(my_users)
    return Response(response,mimetype='application/json')

# en este metodo se realiza un retorno 
@app.route('/users/<id>',methods=['GET'])
def devolver_usuario_id(id):
    usuario = mongo.db.users.find_one({'_id': ObjectId(id)}) # el find one devuelve el primer usuario que coincida
    response = json_util.dumps(usuario)
    return Response(response,mimetype='application/json')


@app.route('/users/<id>',methods=['DELETE'])
def borrar_usuario(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'user '+ id + ' fue borrado satisfactoriamente'})
    return response

@app.route('/users/<id>',methods=['PUT'])
def actualizacion(id):
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if username and email and password:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one({'_id': ObjectId(id)},)



if __name__ == "__main__":
    app.run(debug=True)