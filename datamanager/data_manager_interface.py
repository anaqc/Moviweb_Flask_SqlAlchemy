from abc import ABC, abstractmethod


class DataMangerInterface(ABC):
    

    def _get_all_users(self):
        """ This function return a list of all users 
        in the database"""
        ...
    

    def _get_user_info(self, id_user):
        """ This function return the information from a user"""
        ...


    def _get_user_movies(self, search_id_user: int):
        """ This function a list of all movies of a specific user"""
        ...
        
    
    def _add_user(self, user_name: str):
        """ This function add a new user in the database"""
        ...


    def _add_movie(self,movie_id_user, movie_name, movie_director, movie_year, movie_rating,
                   movie_poster,  movie_imdb_id ):
        """ This function add a new movie in the database"""
        ...


    def _get_user_movie(self, user_id, movie_id):
        """ This function return the details of a specific movie in the database"""
        ...


    def _update_movie(self,user_id, movie_id: int, movie_name: str = None, movie_director: str 
                      = None, movie_year: int = None, movie_rating: int = None, 
                      movie_poster:str=None, movie_imdb_id:str=None):
        """ This function update the datails of a 
        specific movie in the database"""
        ...


    def _delete_movie(self, movie_id, user_id):
        """ This function delete a specific movie from a 
        the database"""
        ...
    

    def _delete_usser(self, user_id):
        """ This function delete a specific user from
        the database"""
        ...
    

    def _add_genre(self, name, details=None):
        """ This function add a new genre in the database"""
        ...
        

    def _delete_genre(self, genre_id):
        """ This function delete the genre by id"""
        ...
        
        
    def _get_all_movie_genres(self):
        """ this function get a list of all the movie genres"""
        ...
    

    def _add_review(self, user_id, movie_id, awards, review_text):
        """ This functi0on add a new review to the database"""
        ...
    
    
    def _update_review(self, review_id, awards, review_text:str = None):
        """ This function update the movie  rating and review text"""
        ...
    

    def _delete_review(self, user_id, movie_id):
        """ This function delete a specific review from
        the database"""
        ...
    

    def _get_movie_review(self, user_id, movie_id):
        """ This function return the details of a movie review"""
        ...

        