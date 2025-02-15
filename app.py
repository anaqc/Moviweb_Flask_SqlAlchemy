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
    

@app.route("/add_user",methods=["GET","POST"])
def add_user():
    """ This route present a form that enables the addiotion
    of a new user to the MovieWeb App"""
    if request.method == "POST":
        name = request.form.get("user_name")
        try:
            if data_manager.add_user(name):
                message = f"User {name} added successfully!"
            else:
                message = f"User {name} already exist!"
            render_template("add_user.html", message=message)
        except Exception as e:
            message = f"Error: {e}"
            render_template("add_user.html", message=message)
    return render_template("add_user.html")

@app.route("/users/<int:user_id>/add_movie", methods=["GET", "POST"])
def add_movie(user_id):
    """ This route display a form to add a new movie to a 
    users movies"""
    if request.method == "POST":
        try:
            name = request.form.get("movie_name")
            director = request.form.get("movie_director")
            year = int(request.form.get("movie_year"))
            rating = int(request.form.get("movie_rating"))
            data_manager.add_movie(name, director, year, rating, user_id)
            message = f"Movie {name} added successfully!"
            render_template("add_movie.html", message=message)
        except Exception as e:
            message = f"Error: {e}"
            render_template("add_movie.html", message=message)
    render_template("add_movie.html")


@app.route("/users/<int: user_id>/update_movie/<int: movie_id>", methods=["GET", "PUT"])
def update_user_movie(update_user_id, update_movie_id):
    """ this route display a form allowing for the updating of 
    details of a specific movie in a user list"""
    if request.method == "PUT":
        try: 
            movie = data_manager.update_movie(
                user_id = update_user_id,
                movie_id = update_movie_id,
                movie_name = request.form.get("movie_name"),
                movie_director = request.form.get("movie_director"),
                movie_year = int(request.form.get("movie_year")),
                movie_rating = int(request.form.get("movie_rating"))
            )
            if movie:
                message = f"Movie {movie.name} updated successfully!"
                render_template("update_movie.html", message=message)
        except ValueError as e: 
            render_template("update_movie.html", message=e)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)