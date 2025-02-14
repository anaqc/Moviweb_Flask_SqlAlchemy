from flask import Flask, request, render_template
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
    return render_template("users.html", users=users)


@app.route("/users/<int:user_id>")
def user_movies(user_id):
    """ This route present a list of specific user favorite movies"""
    list_movies_user = data_manager.get_user_movies(user_id)
    return list_movies_user
    

@app.route("/add_user",methods=["POST"])
def add_user():
    """ This route present a form that enables the addiotion
    of a new user to the MovieWeb App"""
    name = request.form.get("user_name")
    try:
        if data_manager.add_user(name):
            message = f"User {name} added successfully!"
        else:
            message = f"User {name} already exist!"
        render_template("add_user.html", message=message)
    except Exception as e:
        message = f"Error: {e}"






if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)