from sqlalchemy import create_engine
from datamanager.data_manager_interface import DataMangerInterface
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from models.movie import Movie
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


    def get_all_users(self):
        """ This function return a list of all users 
        in the database"""
        all_users = self.session.query(User).all()
        return all_users
    

    def get_user_movies(self, search_id_user: int):
        """ This function a list of all movies of a specific user"""
        # Check if user exist    
        user  = self.session.query(User).filter(User.id == search_id_user).one()
        if user:
            user_movies = self.session.query(Movie).filter(Movie.id_user == search_id_user).all()
            return user_movies
        raise ValueError(f"User {user.id} not exist")
        
    
    def add_user(self, user_name: str):
        """ This function add a new user in the database"""
        try: 
            if not user_name:
                raise ValueError("User name must be a non-empty string")
            user_name_exist = self.session.query(User).filter(User.name == user_name).first()
            if user_name_exist:
                return None
            new_user = User(name=user_name)
            self.session.add(new_user)
            self.session.commit()
            return new_user
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Unexpected error while adding user: {str(e)}")


    def add_movie(self, movie_name, movie_director, movie_year, movie_rating, movie_id_user):
        """ This function add a new movie in the database"""
        try: 
            new_movie = Movie(
                            name=movie_name,
                            director=movie_director,
                            year=movie_year,
                            rating=movie_rating,
                            id_user=movie_id_user 
                        )
            self.session.add(new_movie)
            self.session.commit()
            return new_movie
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Unexpected error adding the movie: {str(e)}")


    def get_user_movie(self, user_id, movie_id):
        """ This function return the details of a specific movie in the database"""
        query = self.session.query(User, Movie).join(Movie).filter(
            User.id ==user_id,
            Movie.id == movie_id
        ).first()
        if query:
            return query[1]
        raise ValueError(f"movie id: {movie_id} or user id: {user_id} not exist!")


    def update_movie(self,user_id, movie_id: int, movie_name: str = None, movie_director: str = None,
                      movie_year: int = None, movie_rating: int = None):
        """ This function update the datails of a 
        specific movie in the database"""
        movie = self.session.query(User, Movie).join(Movie).filter(
            User.id == user_id, 
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
            self.session.commit()
            return movie
        raise ValueError(f"movie id: {movie_id} or user id: {user_id} not exist!")


    def delete_movie(self, movie_id):
        """ This function delete a specific movie from a 
        the database"""
        movie = self.session.query(Movie).get(movie_id)
        if movie:
            self.session.delete(movie)
            self.session.commit()
            return True
        return False
    

    def delete_usser(self, user_id):
        """ This function delete a specific user from
        the database"""
        user = self.session.query(User).get(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False

