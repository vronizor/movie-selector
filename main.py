import json
import random
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from typing import List, Dict
from pathlib import Path

app = FastAPI()

# app.mount(
#     "/static",
#     StaticFiles(directory=Path(__file__).parent.absolute() / "static"),
#     name="static",
# )

# Load the JSON data
# with open('imdb_top250.json', 'r') as file:
#     movies = json.load(file)

@app.get("/movies", response_model=List[Dict])
async def get_movies(skip: int = 0, limit: int = 10):
    return movies[skip: skip + limit]

@app.get("/movies/{rank}", response_model=Dict)
async def get_movie(rank: int):
    for movie in movies:
        print(movie["rank"])  # Debugging print statement
        if movie["rank"] == rank:
            return movie
    raise HTTPException(status_code=404, detail="Movie not found")

@app.get("/search", response_model=List[Dict])
async def search_movies(query: str):
    return [movie for movie in movies if query.lower() in movie["title"].lower()]

@app.get("/")
def read_root(request: Request):
    with open("index.html", "r") as f:
        html_content = f.read()
    return Response(content=html_content, media_type="text/html")

# @app.get("/random_movies")
# def get_random_movies(num_movies: int):
#     with open("imdb_top250.json", "r") as f:
#         imdb_top250 = json.load(f)
#     random_movies = random.sample(imdb_top250, num_movies)
#     return {"random_movies": random_movies}

imdb_top250 = json.load(open("imdb_top250.json", "r"))
bfi_top250 = json.load(open("bfi_top250.json", "r"))
rotten_top300 = json.load(open("rotten_top300.json", "r"))

@app.get("/random_movies")
def get_random_movies(num_movies: int, imdb_checkbox: bool, bfi_checkbox: bool, rotten_checkbox: bool):
    movies = []
    if imdb_checkbox:
        movies.extend(imdb_top250)
    if bfi_checkbox:
        movies.extend(bfi_top250)
    if rotten_checkbox:
        movies.extend(rotten_top300)
    random_movies = random.sample(movies, num_movies)
    return {"random_movies": random_movies}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)