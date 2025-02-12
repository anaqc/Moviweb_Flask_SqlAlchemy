from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


# Create base class for declarativr models
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)


    def __str__(self):
        return f"id: {self.id}, name: {self.name}"
