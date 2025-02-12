from flask import Flask 
from SQLite_data_manager import User, Movie, SQLiteDataManager


new_data_manager = SQLiteDataManager("dbmovie.sqlite")

#new_data_manager.add_user("elisa")
#new_data_manager.add_movie("twilight", "Catherine Hardwicke", 2008, 10, 1)
# new_data_manager.add_movie("f", " Hake", 2008, 10, 1)
# users = new_data_manager.get_all_users()
# for user in users:
#     print(user)
# movies = new_data_manager.get_user_movies(1)
# for movie in movies:
#     print(movie)

#new_data_manager.update_movie(movie_id=1, movie_name="Twilight")
#new_data_manager.delete_movie(2)