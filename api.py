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


@api.route("/users/<int:user_id>/movies", methods=["POST"])
def add_user_movie(user_id):
    """ This function add a new favoritr movie for a user"""
    # Get the Json data from the request body
    users = data_manager._get_user_info(user_id)
    if users:
        data = request.json
        if not data or not all(key in data for key in 
                            ["name", "director", "year", "rating", "poster", 
                                "imdb_id", "genres"]):
            return jsonify({"error" : "Missing required fields"}), 400
        if (not isinstance(data["year"], int) or not isinstance(data["rating"], float) 
            or not isinstance(data["genres"], list)):
            return jsonify({"error" : "Error value of required fields"}), 400
        new_movie = data_manager._add_movie(
                    movie_name=data["name"],
                    movie_director=data["director"],
                    movie_year=data["year"],
                    movie_rating=data["rating"],
                    movie_poster=data["poster"],
                    movie_imdb_id=data["imdb_id"],
                    movie_id_user= user_id,
                    movie_genres=data["genres"]
        )
        return jsonify({
            "message" : "Movie add successfully", 
            "movie" : {
                            "id" : new_movie.id,
                            "name" : new_movie.name,
                            "director" : new_movie.director,
                            "year" : new_movie.year,
                            "rating": new_movie.rating,
                            "poster" : new_movie.poster,
                            "imdb_id" : new_movie.imdb_id,
                            "id_user" : new_movie.id_user
                }
            }), 200
    return jsonify({"error" : "User not found"})