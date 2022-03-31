from sqlalchemy import Column, String

from model.base import Base, db


class User(Base, db.Model):
    __tablename__ = "user"

    email = Column(String, unique=True)
    password = Column(String)
    status = Column(String)
