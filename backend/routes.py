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
    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == id:
            return picture
    
    return {"message": "Picture not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.json

    if new_picture is None:
        return {"Message": "Invalid new picture parameter"}

    try:
        for picture in data:
            if picture["id"] == new_picture["id"]:
                return {"Message": f"picture with id {picture['id']} already present"}, 302

        data.append(new_picture)
        json_object = json.dumps(data, indent=4)

        with open(json_url, "w") as outfile:
            outfile.write(json_object)

        return jsonify(new_picture), 201
    except NameError:
        return {"Message": "Invalid new picture json"}, 504

    return {new_picture}, 200

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    new_picture = request.json

    ids = [picture["id"] for picture in data]
    if id not in ids:
        return {"message": "picture not found"}, 404

    try:
        for idx, picture in enumerate(data):
            if picture["id"] == id:

                data[idx]["pic_url"] = new_picture["pic_url"]
                data[idx]["event_country"] = new_picture["event_country"]
                data[idx]["event_state"] = new_picture["event_state"]
                data[idx]["event_city"] = new_picture["event_city"]
                data[idx]["event_date"] = new_picture["event_date"]

        json_object = json.dumps(data, indent=4)
        with open(json_url, "w") as outfile:
            outfile.write(json_object)
    except NameError:
        return {"message": "Invalid picture json"}, 504

    return {"message": "success"}, 200
    
######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):

    ids = [picture["id"] for picture in data]
    if id not in ids:
        return {"message": "picture not found"}, 404

    for picture in data:
        if picture["id"] == id:
            data.remove(picture)

    json_object = json.dumps(data, indent=4)
    with open(json_url, "w") as outfile:
        outfile.write(json_object)

    return {}, 204
    
