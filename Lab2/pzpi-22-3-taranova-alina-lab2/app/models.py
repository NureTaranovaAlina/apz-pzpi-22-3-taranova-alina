from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Text, Float, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    role = Column(String, nullable=False, default="user")

    flashcards = relationship("Flashcard", back_populates="owner")
    crosswords = relationship("Crossword", back_populates="owner")


class Flashcard(Base):
    __tablename__ = "flashcards"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, index=True, nullable=False)
    translation = Column(String, nullable=False)
    definition = Column(Text, nullable=True)
    examples = Column(JSON, nullable=True)
    tags = Column(JSON, nullable=True)
    ef = Column(Float, nullable=False, default=2.5)
    interval = Column(Integer, nullable=False, default=0)
    repetitions = Column(Integer, nullable=False, default=0)
    next_review = Column(Date, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="flashcards")


class Crossword(Base):
    __tablename__ = "crosswords"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    grid = Column(JSON, nullable=False)
    clues = Column(JSON, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="crosswords")


