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


@api.route("/users/<int:user_id>/movies", methods=["GET"])
def list_user_movies(user_id):
    """ This function return a list of favorites movies from a user"""
    movies = data_manager._get_user_movies(user_id)
    list_movies = []
    for movie in movies:
        list_movies.append(
            {
                "id" : movie.id,
                "name" : movie.name,
                "director" : movie.director,
                "year" : movie.year,
                "rating": movie.rating,
                "poster" : movie.poster,
                "imdb_id" : movie.imdb_id,
                "id_user" : movie.id_user
            }
        )
    return jsonify({"user movies" : list_movies})


