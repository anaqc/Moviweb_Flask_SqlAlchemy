from abc import ABC, abstractmethod


class DataMangerInterface(ABC):
    
    

    def get_all_users(self):
        ...


    def get_user_movies(self, user_id):
        ...

    
    def get_all_movies(self):
        ...

    
    def get_user_movies(self):
        ...
    

    def add_user(self, name):
        ...

  
    def add_movie(self, movie_name, movie_director, movie_year, movie_rating):
        ...
