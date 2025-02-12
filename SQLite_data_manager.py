from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.exc import SQLAlchemyError
from data_manager_interface import DataManagerInterface
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime

# Create base class for declarativr models
Base = declarative_base()


class User(Base):
    __table__ = "users"

    id = Column(Integer, primary_key=True, autoincremet=True)
    name = Column(String(50), unique=True, nullable=False)


class Movie(Base):
    __table__ = "movies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150))
    director = Column(String(100))
    year = Column(Integer)
    rating = Column(Integer)
    id_user = Column(Integer, ForeignKey("users.id"), nullable=True)


    def __init__(self, name, director, year, rating):
        self.name = name
        self.director = director
        self.year = year
        self.rating = rating
        now_year = datetime.datetime.now().year
        if not 1000 <= self.year <= now_year:
            raise ValueError("invalid year")
        if not 0 <= self.rating <= 10:
            raise ValueError("invalid rating range")


class SQLiteDataManager(DataManagerInterface):
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


    def get_all_users(self) -> list:
        """ This function return a list of all users 
        in the database"""
        all_users = self.session.query(User).all()
        return all_users
    

    def get_user_movies(self, input_user_id: int):
        """ This function a list of all movies of a specific user"""
        user_movies = self.session.query(Movie).filter(user_id = input_user_id).all()
        return user_movies

    
    def add_user(self, user_name):
        """ This function add a new user in the database"""
        try: 
            new_user = User(name=user_name)
            self.session.add(new_user)
            self.session.commit()
            return new_user
        except SQLAlchemyError as e:
            # Rollback changes in case of failure
            self.session.rollback()
            raise RuntimeError(f"Failed to add user: {str(e)}")
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Unexpected error while adding user: {str(e)}")


    def add_movie(self, movie_name, movie_director, movie_year, movie_rating):
        """ This function add a new movie in the database"""
        try: 
            new_movie = Movie(
                            name=movie_name,
                            director=movie_director,
                            year=movie_year,
                            rating=movie_rating 
                        )
            self.session.add(new_movie)
            self.session.commit()
            return new_movie
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f"Failed to add user: {str(e)}")
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Unexpected error adding the movie: {str(e)}")


        