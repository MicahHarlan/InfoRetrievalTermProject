from typing import List, Optional
from pydantic import BaseModel, Field

# Forward declare models for circular references

class GenreBase(BaseModel):
    genreName: str

class Genre(GenreBase):
    genreName: str
    class Config:
        orm_mode = True

class ActorBase(BaseModel):
    ActorID: str
    Name: str


class Actor(ActorBase):
    ActorID: str
    Name: str
    class Config:
        orm_mode = True


class DirectorBase(BaseModel):
    DirectorID: str
    Name: str

class Director(DirectorBase):
    DirectorID: str
    Name: str
    class Config:
        orm_mode = True

class MovieBase(BaseModel):
    primaryTitle: str
    Year: int
    originalTitle: str
    runtimeMinutes: int
    avgRating: float
    numVotes: int
    plot: str | None
    image: str | None
    genres: List[Genre] = []
    actors: List[Actor] = []
    directors: List[Director] = []

class Movie(MovieBase):
    MovieID: str
    class Config:
        orm_mode = True