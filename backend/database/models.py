# Defines the database models for users, words, games, and guesses.

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from .connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    role = Column(
        String(10),
        nullable=False,
        default="PLAYER"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

#root word to be guessed
class Word(Base):
    __tablename__ = "words"

    id = Column(
        Integer,
        primary_key=True
    )

    word = Column(
        String(5),
        unique=True,
        nullable=False
    )

class Game(Base):
    __tablename__ = "games"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    word_id = Column(
        Integer,
        ForeignKey("words.id"),
        nullable=False
    )

    started_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    completed_at = Column(
        DateTime,
        nullable=True
    )

    status = Column(
        String(20),
        default="IN_PROGRESS",
        nullable=False
    )

    number_of_guesses = Column(
        Integer,
        default=0,
        nullable=False
    )

#user word to checked with the root word
class Guess(Base):
    __tablename__ = "guesses"

    id = Column(
        Integer,
        primary_key=True
    )

    game_id = Column(
        Integer,
        ForeignKey("games.id"),
        nullable=False
    )

    guessed_word = Column(
        String(5),
        nullable=False
    )

    guess_number = Column(
        Integer,
        nullable=False
    )

    guessed_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )