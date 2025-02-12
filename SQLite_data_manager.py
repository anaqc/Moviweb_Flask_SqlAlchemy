from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.exc import SQLAlchemyError
from data_manager_interface import DataMangerInterface
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime

# Create base class for declarativr models
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)


    def __str__(self):
        return f"id: {self.id}, name: {self.name}"


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150))
    director = Column(String(100))
    year = Column(Integer)
    rating = Column(Integer)
    id_user = Column(Integer, ForeignKey("users.id"), nullable=True)


    def __init__(self, name, director, year, rating, id_user):
        self.name = name
        self.director = director
        self.year = year
        self.rating = rating
        self.id_user = id_user
        now_year = datetime.datetime.now().year
        if not 1000 <= self.year <= now_year:
            raise ValueError("invalid year")
        if not 0 <= self.rating <= 10:
            raise ValueError("invalid rating range")
        
    
    def __str__(self):
        return f"id: {self.id}, name: {self.name}, director: {self.director}, year: {self.year}"


class SQLiteDataManager(DataMangerInterface):
    def __init__(self, db_file_name):
        # Create a engine for SQLite database
        self.engine = create_engine(f"sqlite:///data/{db_file_name}")
        # Create a database session 
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        # Create base for declarative models
        self.Base = declarative_base()
        # create all tables..
        Base.metadata.create_all(self.engine)


    def get_all_users(self):
        """ This function return a list of all users 
        in the database"""
        all_users = self.session.query(User).all()
        return all_users
    

    def get_user_movies(self, search_id_user: int):
        """ This function a list of all movies of a specific user"""
        user_movies = self.session.query(Movie).filter(Movie.id_user == search_id_user).all()
        return user_movies

    
    def add_user(self, user_name):
        """ This function add a new user in the database"""
        try: 
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


        