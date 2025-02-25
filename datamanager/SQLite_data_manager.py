from sqlalchemy import create_engine, exc
from datamanager.data_manager_interface import DataMangerInterface
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from models.movie import Movie, Genre, Review
from models.user import User
from models.base import Base


class SQLiteDataManager(DataMangerInterface):
    def __init__(self, db_file_name):
        # Create a engine for SQLite database
        self.engine = create_engine(f"sqlite:///data/{db_file_name}")
        # Create a database session 
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        # Create base for declarative models
        # self.Base = declarative_base()
        # create all tables..
        Base.metadata.create_all(self.engine)


    def _get_all_users(self):
        """ This function return a list of all users 
        in the database"""
        all_users = self.session.query(User).all()
        return all_users


    def _get_user_info(self, id_user):
        """ This function return the information from a user"""
        return self.session.query(User).filter(User.id == id_user).one()


    def _get_user_movies(self, search_id_user: int):
        """ This function a list of all movies of a specific user"""
        # Check if user exist 
        if self._get_user_info(search_id_user):    
            user_movies = self.session.query(Movie).filter(Movie.id_user == search_id_user).all()
            return user_movies
        
    
    def _add_user(self, user_name: str, user_password: str):
        """ This function add a new user in the database"""
        try: 
            if not user_name:
                raise ValueError("User name must be a non-empty string")
            user_name_exist = self.session.query(User).filter(User.name == user_name).first()
            if user_name_exist:
                return None
            
            new_user = User(name=user_name)
            new_user.password = user_password
            self.session.add(new_user)
            self.session.commit()
            return new_user
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Unexpected error while adding user: {str(e)}")


    def _add_movie(self,movie_id_user, movie_name, movie_director, movie_year, 
                   movie_rating,movie_poster, movie_imdb_id, movie_genres):
        """ This function add a new movie in the database"""
        try: 
            list_genres = []

            for genre in movie_genres: 
                if self._check_genre(genre):
                    list_genres.append(self.session.query(Genre).filter(
                        Genre.name == genre.capitalize()).one())
                else:
                    new_genre = self._add_genre(genre.capitalize())
                    list_genres.append(new_genre)
            print(list_genres)
            new_movie = Movie(
                            name=movie_name,
                            director=movie_director,
                            year=movie_year,
                            rating=movie_rating,
                            poster=movie_poster,
                            imdb_id=movie_imdb_id,
                            id_user=movie_id_user
                        )
            new_movie.genres.extend(list_genres)
            self.session.add(new_movie)
            self.session.commit()
            return new_movie
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Unexpected error adding the movie: {str(e)}")


    def _check_genre(self, genre):
        """ This function check if a genre exist in the db and if not create a new genre"""
        return self.session.query(Genre).filter(Genre.name == genre.capitalize()).first()
    

    def _get_user_movie(self, user_id, movie_id):
        """ This function return the details of a specific movie in the database"""
        query = self.session.query(User, Movie).join(Movie).filter(
            User.id ==user_id,
            Movie.id == movie_id
        ).first()
        if query:
            return query[1]
        raise ValueError(f"movie id: {movie_id} or user id: {user_id} not exist!")


    def _update_movie(self,user_id, movie_id: int, movie_name: str = None, 
                      movie_director: str = None, movie_year: int = None, 
                      movie_rating: int = None, movie_poster: str = None, movie_imdb_id: str = None):
        """ This function update the datails of a 
        specific movie in the database"""
        movie = self.session.query(Movie).filter(
            Movie.id_user == user_id, 
            Movie.id == movie_id
            ).first()
        if movie:
            if movie_name:
                movie.name = movie_name 
            if movie_director:
                movie.director = movie_director
            if movie_year:
                movie.year = movie_year
            if movie_rating:
                movie.rating = movie_rating
            if movie_poster:
                movie.poster = movie_poster
            if movie_imdb_id:
                movie.imdb_id = movie_imdb_id    
            self.session.commit()
            return movie
        raise ValueError(f"movie id: {movie_id} or user id: {user_id} not exist!")


    def _delete_movie(self, movie_id, user_id):
        """ This function delete a specific movie from a 
        the database"""
        movie = self.session.query(Movie).filter(
            Movie.id == movie_id,
            Movie.id_user == user_id
        ).first()
        if movie:
            self.session.delete(movie)
            self.session.commit()
            return True
        raise ValueError(f"movie id: {movie_id} or user id: {user_id} not exist!")
    

    def _delete_usser(self, user_id):
        """ This function delete a specific user from
        the database"""
        user = self.session.query(User).get(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        raise ValueError(f"User id: {user_id} not exist!")
    

    def _add_genre(self, name, details=None):
        """ This function add a new genre in the database"""
        try: 
            new_genre = Genre(name.capitalize(), details)
            self.session.add(new_genre)
            self.session.commit()
            return new_genre
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Unexpected error adding the movie genre: {str(e)}")
        

    def _delete_genre(self, genre_id):
        """ This function delete the genre by id"""
        genre = self.session.query(Genre).get(genre_id)
        if genre:
            self.session.delete(genre)
            self.session.commit()
            return True
        raise ValueError(f"Genre id: {genre_id} not exist!")
        
        
    def _get_all_movie_genres(self):
        """ this function get a list of all the movie genres"""
        return self.session.query(Genre).all()
    

    def _add_review(self, user_id, movie_id, awards, review_text):
        """ This functi0on add a new review to the database"""
        try:
            new_review = Review(user_id, movie_id, awards, review_text)
            self.session.add(new_review)
            self.session.commit()
            return new_review
        except Exception as e:
            self.session.rollback()
            raise Exception(f"unexpected error adding the review: {str(e)}")
    
    
    def _update_review(self, review_id, awards, review_text:str = None):
        """ This function update the movie  rating and review text"""
        review = self.session.query(Review).filter(Review.id == review_id).first()
        if review:
            if awards:
                review.awards = awards
            if review_text:
                review.review_text = review_text
            self.session.commit()
            return review
        raise ValueError(f"review id: {review_id} not exist!")
    

    def _delete_review(self, user_id, movie_id):
        """ This function delete a specific review from
        the database"""
        review = self.session.query(Review).filter(
            Review.movie_id == movie_id,
            Review.user_id == user_id
        ).first()
        if review:
            self.session.delete(review)
            self.session.commit()
            return True
        raise ValueError(f"movie id: {movie_id} or user id: {user_id} not exist!")
    

    def _get_movie_review(self, user_id, movie_id):
        """ This function return the details of a movie review"""
        review_movie = self.session.query(Review).filter((Review.user_id == user_id) &
                                                          (Review.movie_id == movie_id)).first()
        if review_movie:
            return review_movie
        return None



