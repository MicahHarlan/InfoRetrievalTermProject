from fastapi import Depends, FastAPI, Request, Response
from sqlalchemy.orm import Session

import schemas
import models
import crud
import search
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

def get_db(request: Request):
    return request.state.db

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/movies/", response_model=list[schemas.Movie])
def read_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    movies = crud.getMovies(db, skip=skip, limit=limit)
    return movies

@app.get("/movies/{movie_id}", response_model=schemas.Movie)
def read_movie(movie_id: str, db: Session = Depends(get_db)):
    movie = crud.getMovieById(db, movie_id)
    return movie

@app.get("/directors/", response_model=list[schemas.Director])
def read_directors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    directors = crud.getDirectors(db, skip=skip, limit=limit)
    return directors

@app.get("/search", response_model=list[schemas.Movie])
def query(q: str, db: Session = Depends(get_db)):
    # Full match

    first_shot = []
    full_match_title = crud.getMovieIdsByTitle(db, q)
    for movie_id, *_ in full_match_title:
        first_shot.append(movie_id)

    full_match_plot = crud.getMovieIdsByPlot(db, q)
    for movie_id, *_ in full_match_plot:
        first_shot.append(movie_id)

    full_match_actor = crud.getMovieIdsByActor(db, q)
    for movie_id, *_ in full_match_actor:
        first_shot.append(movie_id)

    movies = []
    for movie_id in first_shot:
        movie = crud.getMovieById(db, movie_id)
        movies.append(movie)
    if len(movies) > 0:
        return movies

    print(q)
    # Parse
    qs = search.parse_query(q)

    # Search

    movie_ids_title_matched = []
    movie_ids_actor_matched = []
    movie_ids_director_matched = []
    movie_ids_plot_matched = []

    # 1st shot - Title
    for word in qs:
        result_tuples = crud.getMovieIdsByTitle(db, word)
        for movie_id, *_ in result_tuples:
            movie_ids_title_matched.append(movie_id)

    # 2nd shot - Actor
    # for word in qs:
    #     movie_ids_actor_matched = crud.getMovieIdsByActor(db, word)
    #
    # # 3rd shot - Director
    # for word in qs:
    #     movie_ids_director_matched = crud.getMovieIdsByDirector(db, word)
    #
    # # 4th shot - Plot
    # for word in qs:
    #     movie_ids_plot_matched = crud.getMovieIdsByPlot(db, word)

    movie_ids = set(movie_ids_title_matched + movie_ids_actor_matched + movie_ids_director_matched + movie_ids_plot_matched)
    for movie_id in movie_ids:
        movie = crud.getMovieById(db, movie_id)
        movies.append(movie)
    return movies

    # query = query_parser.parse_query(q)
    # collector = Collector.top_docs(10)
    # search_result = index.searcher().search(query, collector)
    #
    # documents = [DocumentOut(**doc) for doc in search_result.docs()]
    # return documents
    # movies = crud.getMovieById(db, "tt0020827")
    # return [movies]
