from flask import Flask, request, render_template, redirect, url_for
from datamanager.SQLite_data_manager import SQLiteDataManager
from sqlalchemy.exc import NoResultFound
from datamanager.data_OMDb_API import OMDb_api


app = Flask(__name__)
data_manager = SQLiteDataManager("moviwebapp.sqlite")


@app.route("/", methods=["GET","POST"])
def home():
    user_name = request.form.get("user_name","")
    user_password = request.form.get("user_password")
    if user_name:
        users = data_manager._get_all_users()
        for user in users:
            if user_name == user.name and user.verify_password(user_password):
                return redirect(url_for("user_movies", user_id=user.id)) 
        message = f"User {user_name} not exist!" 
        return render_template("home.html", message=message)
    return render_template("home.html")


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
    """ This route present a form that enables the addition
    of a new user to the MovieWeb App"""
    try:
        if request.method == "POST":
            name = request.form.get("user_name")
            password = request.form.get("user_password")
            if data_manager._add_user(name, password):
                return render_template("home.html")
            else:
                message = f"User {name} or password incorrect!"
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
            year = int(movie_year) if movie_year.isdigit() else 0
            rating_movie = request.form.get("movie_rating")
            rating = float(rating_movie)
            poster = request.form.get("movie_poster")
            imdb_id = request.form.get("movie_imdb_id")
            genres = request.form.get("movie_genres").split(", ")
            data_manager._add_movie(user_id, name, director, year, rating, poster, imdb_id, genres)
            movie_name_search = ""
            return redirect(url_for("user_movies",user_id=user_id))
        if movie_name_search:
            list_movies = OMDb_api.request_movie_search(movie_name_search)
    
            return render_template("add_movie.html", user_id=user_id, list_movies=list_movies,
                                    movie_name_search=movie_name_search)
        return render_template("add_movie.html", user_id=user_id, movie_rating="5",
                                movie_name_search=movie_name_search)
    except NoResultFound as e:
        return render_template("404.html", error=str(e))
    except Exception as e:
        return render_template("404.html", error=str(e))


@app.route("/movie_genre", methods=["GET", "POST"])
def movie_genre():
    """ This route display a form to add a movie genre and the alist of all the genres added"""
    try:
        movie_genres = data_manager._get_all_movie_genres()
        if request.method == "POST":
            name = request.form.get("genre_name")
            details = request.form.get("genre_details")
            data_manager._add_genre(name, details)
            return render_template("movie_genre.html", movie_genres=movie_genres)
        return render_template("movie_genre.html", movie_genres=movie_genres)
        
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


@app.route("/users/<int:user_id>/add_review/<int:movie_id>", methods=["GET", "POST"])
def add_review(user_id, movie_id):
    """ This route add a review to a specific movie"""
    try:
        movie_user = data_manager._get_user_movie(user_id, movie_id)
        if request.method == "POST" and request.form.get("movie_awards"):
            awards = request.form.get("movie_awards")
            review_text = request.form.get("movie_review_text")
            movie_id = request.form.get("movie_id")
            user_id = request.form.get("user_id")
            data_manager._add_review(user_id, movie_id, awards,review_text)
            return redirect(url_for("user_movies", user_id=user_id))
        return render_template("add_review.html", movie_user=movie_user, user_id=user_id, movie_id=movie_id)
    except ValueError as e:
        return render_template("404.html", error=str(e))
    except IOError as e:
        # Code to handle the exception
        print("An IOError occurred: ", str(e))
        return render_template("404.html", error=str(e))
    except Exception as e:
        return render_template("404.html", error=str(e))


@app.route("/users/<int:user_id>/update_review/<int:movie_id>",methods=["GET", "POST"])
def update_review(user_id, movie_id):
    """ This route display a form allowing for the updating of
    details of a specific movie review"""
    try:
        movie_user = data_manager._get_user_movie(user_id, movie_id)
        movie_review = data_manager._get_movie_review(user_id, movie_id)
        if movie_review:
            if request.method == "POST" and request.form.get("_method") == "PUT":
                review = data_manager._update_review(
                awards = request.form.get("movie_awards"),
                review_text = request.form.get("movie_review_text"),
                review_id=movie_review.id
                )
                if review:
                    return redirect(url_for("user_movies", user_id=user_id))
            return render_template("update_review.html", movie_review=movie_review, movie_user=movie_user, user_id=user_id)
        return redirect(url_for("add_review", user_id=user_id, movie_id=movie_id))
    except ValueError as e:
        return render_template("404.html", error=str(e))
    except IOError as e:
        # Code to handle the exception
        print("An IOError occurred: ", str(e))
        return render_template("404.html", error=str(e))
    except Exception as e:
        return render_template("404.html", error=str(e))

@app.route("/users/<int:user_id>/delete_review/<int:movie_id>", methods=["POST"])
def delete_review(user_id, movie_id):
    try:
        if data_manager._delete_review(user_id, movie_id):
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