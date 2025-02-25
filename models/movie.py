from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship
import datetime
from models.base import Base


class Movie_Genres(Base):
    __tablename__ = "movie_genres"

    movie_id = Column(Integer, ForeignKey("movies.id"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id"), primary_key=True)
  

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150))
    director = Column(String(100))
    year = Column(Integer)
    rating = Column(Float)
    poster = Column(String(200))
    imdb_id = Column(String(15))
    id_user = Column(Integer, ForeignKey("users.id"), nullable=True)


    # relationship with genres
    genres = relationship("Genre", secondary="movie_genres", back_populates="movies")


    def __init__(self, id_user, name, director=None, year=None, rating=0, poster=None,imdb_id=None):
        self.name = name
        self.director = director
        self.year = year
        self.rating = rating
        self.id_user = id_user
        self.poster = poster
        self.imdb_id = imdb_id
        now_year = datetime.datetime.now().year
        if self.year and not 0 <= self.year <= now_year:
            raise ValueError(f"invalid year: {self.year}")
        if self.rating and not 0 <= self.rating <= 10:
            raise ValueError(f"invalid rating range: {self.rating}")
        
    
    def __str__(self):
        return f"id: {self.id}, name: {self.name}, director: {self.director}, year: {self.year}"
  

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    details = Column(String(150))


    # Relationship with movies
    movies = relationship("Movie", secondary="movie_genres", back_populates="genres")


    def __init__(self, name, details=None):
        self.name = name
        self.details = details


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=True)
    awards = Column(String(200))
    review_text = Column(String(500))


    def __init__(self, user_id, movie_id, awards, review_text):
        self.user_id = user_id
        self.movie_id = movie_id
        self.awards = awards
        self.review_text = review_text

