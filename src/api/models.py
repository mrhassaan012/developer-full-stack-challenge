from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from database import Base

# Define the association table for the many-to-many relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    author_id = Column(Integer, ForeignKey("author.id"), back_populates="books")

    author = relationship("Author")
