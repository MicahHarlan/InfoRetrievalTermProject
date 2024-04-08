# crud.py
from sqlalchemy.orm import Session
import sqlalchemy.orm as _orm
import models


def getMovies(db: _orm.Session, skip: int = 0, limit: int = 100):
    return db.query(models.Movie).offset(skip).limit(limit).all()

def getMovieById(db: Session, movie_id: str):
    return db.query(models.Movie).filter(models.Movie.MovieID == movie_id).first()

def getActors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Actor).offset(skip).limit(limit).all()

def getActorById(db: Session, actor_id: str):
    return db.query(models.Actor).filter(models.Actor.ActorID == actor_id).first()
