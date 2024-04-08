from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime, Boolean, Text, SmallInteger, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import NullType

Base = declarative_base()


class Movie(Base):
    __tablename__ = 'Movie'
    MovieID = Column(String, primary_key=True)
    primaryTitle = Column(String)
    Year = Column(Integer)
    originalTitle = Column(String)
    runtimeMinutes = Column(Integer)
    avgRating = Column(Float)
    numVotes = Column(Integer)
    plot = Column(Text)
    image = Column(String)
    genres = relationship('Genre', secondary='MovieGenres', back_populates='movies')
    actors = relationship('Actor', secondary='MovieActors', back_populates='movies')
    directors = relationship('Director', secondary='MovieDirectors', back_populates='movies')

class Genre(Base):
    __tablename__ = 'genres'
    genreName = Column(String, primary_key=True)
    movies = relationship('Movie', secondary='MovieGenres', back_populates='genres')

class MovieGenres(Base):
    __tablename__ = 'MovieGenres'
    MovieID = Column(String, ForeignKey('Movie.MovieID'), primary_key=True)
    genreName = Column(String, ForeignKey('genres.genreName'), primary_key=True)

class Actor(Base):
    __tablename__ = 'Actors'
    ActorID = Column(String, primary_key=True)
    Name = Column(String)
    movies = relationship('Movie', secondary='MovieActors', back_populates='actors')

class MovieActors(Base):
    __tablename__ = 'MovieActors'
    MovieID = Column(String, ForeignKey('Movie.MovieID'), primary_key=True)
    ActorID = Column(String, ForeignKey('Actors.ActorID'), primary_key=True)

class Director(Base):
    __tablename__ = 'Directors'
    DirectorID = Column(String, primary_key=True)
    Name = Column(String)
    movies = relationship('Movie', secondary='MovieDirectors', back_populates='directors')

class MovieDirectors(Base):
    __tablename__ = 'MovieDirectors'
    MovieID = Column(String, ForeignKey('Movie.MovieID'), primary_key=True)
    DirectorID = Column(String, ForeignKey('Directors.DirectorID'), primary_key=True)

