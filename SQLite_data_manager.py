from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String
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
        self.engine = create_engine(f"sqlite:///{db_file_name}")
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
    
    