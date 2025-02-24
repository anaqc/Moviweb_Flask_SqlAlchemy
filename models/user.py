from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from models.base import Base
from passlib.hash import bcrypt_sha256


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(50), nullable=False)


    @property
    def password(self):
        raise AttributeError("Password is not readable")
    

    @password.setter
    def password(self, password):
        # hash the password before storing
        self.password_hash = bcrypt_sha256.hash(password)


    def verify_password(self, password):
        return bcrypt_sha256.verify(password, self.password_hash)


    def __str__(self):
        return f"id: {self.id}, name: {self.name}"


