# crud.py
from sqlalchemy.orm import Session
import sqlalchemy.orm as _orm
import models

def getMovieByTitleAndYear(db: _orm.Session, title: str, year: int):
    return db.query(models.Movie).filter(models.Movie.primaryTitle == title).filter(models.Movie.Year == year).first()

def getMovies(db: _orm.Session, skip: int = 0, limit: int = 100):
    return db.query(models.Movie).offset(skip).limit(limit).all()

def getMovieById(db: Session, movie_id: str):
    return db.query(models.Movie).filter(models.Movie.MovieID == movie_id).first()

def getActors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Actor).offset(skip).limit(limit).all()

def getActorById(db: Session, actor_id: str):
    return db.query(models.Actor).filter(models.Actor.ActorID == actor_id).first()

def getDirectors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Director).offset(skip).limit(limit).all()


def getMovieIdsByTitle(db, q):
    return db.query(models.Movie.MovieID).filter(models.Movie.primaryTitle.like(f'%{q}%')).order_by(models.Movie.numVotes.desc()).limit(10).all()


def getMovieIdsByPlot(db, q):
    return db.query(models.Movie.MovieID).filter(models.Movie.plot.like(f'%{q}%')).order_by(models.Movie.numVotes.desc()).limit(10).all()


def getMovieIdsByActor(db, q):
    return db.query(models.Movie.MovieID).join(models.Movie.actors).filter(models.Actor.Name.like(f'%{q}%')).order_by(models.Movie.numVotes.desc()).limit(10).all()
