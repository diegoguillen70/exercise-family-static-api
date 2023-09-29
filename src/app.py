"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():    
    # this is how you can use the Family datastructure by calling its methods
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as e:        
        return jsonify({"msg": "There was an error getting the members, error: "+ str(e)}), 500
    
@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    try:
        member = jackson_family.get_member(id)
        if member is None:
            raise APIException("Member not found", status_code=404)
        return jsonify(member), 200
    except Exception as e:        
        return jsonify({"msg": "There was an error getting the member, error: "+ str(e)}), 500
    
@app.route('/member', methods=['POST'])
def add_member():
    try:
        member = request.get_json()
        if member is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)        
        if member["first_name"] is None:
            raise APIException("You need to specify the first_name", status_code=400)
        if member["age"] is None:
            raise APIException("You need to specify the age", status_code=400)
        if member["lucky_numbers"] is None:
            raise APIException("You need to specify the lucky_numbers", status_code=400)        
        member = jackson_family.add_member(member)
        return jsonify(member), 200
    except Exception as e:        
        return jsonify({"msg": "There was an error adding the member, error: "+ str(e)}), 500

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    try:        
        member = jackson_family.delete_member(id)
        if member is None:
            raise APIException("Member not found", status_code=404)
        return {"done": True}, 200
    except Exception as e:        
        return jsonify({"msg": "There was an error deleting the member, error: "+ str(e)}), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
