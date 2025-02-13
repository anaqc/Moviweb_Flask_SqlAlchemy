from flask import Flask 
from datamanager.SQLite_data_manager import SQLiteDataManager


app = Flask(__name__)
data_manager = SQLiteDataManager("moviwebapp.sqlite")


# data_manager.add_user("elisa")
# data_manager.add_movie("twilight", "Catherine Hardwicke", 2008, 10, 1)


# new_data_manager.add_movie("f", " Hake", 2008, 10, 1)
# users = new_data_manager.get_all_users()
# for user in users:
#     print(user)
# movies = new_data_manager.get_user_movies(1)
# for movie in movies:
#     print(movie)
#new_data_manager.update_movie(movie_id=1, movie_name="Twilight")
#new_data_manager.delete_movie(2)


@app.route("/")
def home():
    return "Welcome to MovieWeb App!"


@app.route("/users")
def list_users():
    """ This flask route list all users registered in 
    the MovieWeb App"""
    users = data_manager.get_all_users()
    return users


@app.route("/users/<int:user_id>")
def user_movies(user_id):
    """ This route present a list of specific user favorite movies"""
    list_movies_user = data_manager.get_user_movies(user_id)
    return list_movies_user
    



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)