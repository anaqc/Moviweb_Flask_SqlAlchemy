from flask import Flask, request, render_template, redirect, url_for
from datamanager.SQLite_data_manager import SQLiteDataManager
from sqlalchemy.exc import NoResultFound
from datamanager.data_OMDb_API import OMDb_api


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


@app.route("/users", methods=["GET"])
def list_users():
    """ This flask route list all users registered in 
    the MovieWeb App"""
    try: 
        users = data_manager._get_all_users()
        return render_template("users.html", users=users)
    except IOError as e:
        # Code to handle the exception
        print("An IOError occurred: ", str(e))
        return render_template("404.html", error=str(e))
    except Exception as e:
        return render_template("404.html", error=str(e))


@app.route("/users/<int:user_id>", methods=["GET"])
def user_movies(user_id):
    """ This route present a list of specific user favorite movies"""
    try: 
        user = data_manager._get_user_info(user_id)
        list_movies_user = data_manager._get_user_movies(user_id)
        return render_template("user_movies.html", list_movies_user=list_movies_user, user=user)
    except NoResultFound:
        return render_template("404.html")
    except IOError as e:
        # Code to handle the exception
        print("An IOError occurred: ", str(e))
        return render_template("404.html", error=str(e))
    except Exception as e:
        return render_template("404.html", error=str(e))


@app.route("/add_user",methods=["GET","POST"])
def add_user():
    """ This route present a form that enables the addiotion
    of a new user to the MovieWeb App"""
    try:
        if request.method == "POST":
            name = request.form.get("user_name")
            if data_manager._add_user(name):
                message = f"User {name} added successfully!"
            else:
                message = f"User {name} already exist!"
            return render_template("add_user.html", message=message)
        return render_template("add_user.html")
    except IOError as e:
        # Code to handle the exception
        print("An IOError occurred: ", str(e))
        return render_template("404.html", error=str(e))
    except Exception as e:
        return render_template("404.html", error=str(e))


@app.route("/users/<int:user_id>/add_movie", methods=["GET", "POST"])
def add_movie(user_id):
    """ This route display a form to add a new movie to a 
    users movies"""
    try:
        movie_name_search = request.args.get("movie_name_search", "")
        if request.method == "POST":
            name = request.form.get("movie_name")
            director = request.form.get("movie_director")
            movie_year = request.form.get("movie_year")
            year = int(movie_year) if movie_year != "None" else None
            rating_movie = request.form.get("movie_rating")
            rating = float(rating_movie) if rating_movie != "None" else 0
            poster = request.form.get("movie_poster")
            imdb_id = request.form.get("movie_imdb_id")
            data_manager._add_movie(user_id, name, director, year, rating, poster, imdb_id)
            movie_name_search = ""
            return redirect(url_for("user_movies",user_id=user_id))
        if movie_name_search:
            list_movies = OMDb_api.request_movie(movie_name_search)
            print(type(list_movies))
            return render_template("add_movie.html", user_id=user_id, list_movies=list_movies,
                                    movie_name_search=movie_name_search)
        return render_template("add_movie.html", user_id=user_id, movie_rating="5",
                                movie_name_search=movie_name_search)
    except NoResultFound as e:
        return render_template("404.html", error=str(e))
    except Exception as e:
        return render_template("404.html", error=str(e))


@app.route("/users/<int:update_user_id>/update_movie/<int:update_movie_id>", 
           methods=["GET","POST", "PUT"])
def update_user_movie(update_user_id, update_movie_id):
    """ this route display a form allowing for the updating of 
    details of a specific movie in a user list"""
    try:    
        movie_user = data_manager._get_user_movie(update_user_id, update_movie_id)
        if request.method == "POST" and request.form.get("_method") == "PUT":
            movie = data_manager._update_movie(
                user_id = update_user_id,
                movie_id = update_movie_id,
                movie_name = request.form.get("movie_name"),
                movie_director = request.form.get("movie_director"),
                movie_year = int(request.form.get("movie_year")),
                movie_rating = float(request.form.get("movie_rating")),
                movie_poster = request.form.get("movie_poster"),
                movie_imdb_id = request.form.get("movie_imdb_id")
            )
            if movie:
                return redirect(url_for("user_movies", user_id=update_user_id))
        return render_template("update_movie.html", movie_user=movie_user)
    except ValueError as e:
        return render_template("404.html", error=str(e))
    except IOError as e:
        # Code to handle the exception
        print("An IOError occurred: ", str(e))
        return render_template("404.html", error=str(e))
    except Exception as e:
        return render_template("404.html", error=str(e))


@app.route("/users/<int:user_id>/delete_movie/<int:movie_id>", methods=["GET", "POST"])
def delete_movie(user_id, movie_id):
    try:
        if data_manager._delete_movie(movie_id, user_id):
            return redirect(url_for("user_movies", user_id=user_id))
    except Exception as e:
        return render_template("404.html", error=str(e))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", error=str(e)), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)