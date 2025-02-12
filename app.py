from flask import Flask 
from SQLite_data_manager import User, Movie, SQLiteDataManager


new_data_namager = SQLiteDataManager("dbmovie.sqlite")
