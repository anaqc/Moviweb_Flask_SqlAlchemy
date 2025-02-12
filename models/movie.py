from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
import datetime
from base import Base


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

