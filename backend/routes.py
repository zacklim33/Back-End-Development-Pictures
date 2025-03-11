from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500



######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if not data:
        return ({"message":"Data obj doesn't exist"}, 500 )
    return (jsonify(data), 200)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if not data:
        return ({"message":"Data obj doesn't exist"}, 500 )
    
    for picture in data:
        if picture["id"] == id:
            return (jsonify(picture), 200)

    return ({"message":"Invalid ID"}, 404 )


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    # check if data object exist
    if not data:
        return ({"message":"Data object not existing"}, 500 )

    # request data from HTTP header
    inputData = request.get_json()

    # check if valid json input
    if not inputData:
        return ({"message": "Missing or invalid JSON input"}, 422)

    #check if picture exist in database, through using its ID
    for picture in data:
        id1=str(picture["id"])
        if inputData["id"] == picture["id"]:
            return (jsonify({"message": f"picture with id {picture['id']} already present"}), 302)
        
    try:
        data.append(inputData)
    except NameError:
        return({"message": "Internal Server error"},500)
    
    # unit test expects the return of inputData, if QA & QC checks pass
    return(inputData, 201)
        

######################################################################
# UPDATE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    # check if global data array was set
    if not data:
        return ({"message":"Data object not set"}, 500)
    
    # check if HTTP json was correctly inserted
    inputData=request.get_json()

    if not inputData:
        return ({"message": "INPUT JSON is problematic"}, 404)

    # to loop through and locate where inputData matches data array    
    for i, picture in enumerate(data):
        if(picture["id"] == id):
            data[i]=inputData
            return ({"message": f"picture {id} was updated"}, 201)
    
    return ({"message": "picture not found"}, 404)


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
     # check if global data array was set
    if not data:
        return ({"message":"Data object not set"}, 500)
    
    # check if HTTP json was correctly inserted
    for picture in data:
        if (picture["id"]==id):
            data.remove(picture)
            return({"message": "data is successfully removed"},204)
        
    return({"message":"picture not found"},404)


######################################################################
# General Global Error
######################################################################
""" 
@app.errorhandler(500)
def errHand(error):
    return {response.json},500
"""