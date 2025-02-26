from flask import Blueprint, jsonify, request
from datamanager.SQLite_data_manager import SQLiteDataManager


api = Blueprint('api', __name__)
data_manager = SQLiteDataManager("moviwebapp.sqlite")


@api.route("/users", methods=["GET"])
def get_users():
    """ This function get all users in the db"""
    users = data_manager._get_all_users()
    list_users = []
    for user in users:
        list_users.append(
            {
                "id" : user.id,
                "namee" : user.name
            }
        )
    # Return JSON response
    return jsonify({"users" : list_users})


