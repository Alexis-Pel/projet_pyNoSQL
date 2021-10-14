from flask import Flask
from pymongo import MongoClient
import os
from vote import vote_main
from find_movies import find_movies
from movies import movies, add_movies, delete_movie
from actors import add_actors, del_actors, actors, edit_actor
from find_actors import find_actors
from assets.pageReturn import page_return

app = Flask(__name__)
host = os.environ["HOST"]
username = os.environ["DB_USER"]
password = os.environ["DB_PASS"]
cluster = os.environ["CLUSTER"]
database_name = os.environ["DB"]
client = MongoClient(f"mongodb+srv://{username}:{password}@{cluster}/{database_name}?retryWrites=true&w=majority")
db = client[database_name]


@app.route("/")
def home():
    return page_return('SUCCESS', 200, 'Accueil')


@app.route("/movies", methods=["GET"])
def movie():
    return movies(db)


@app.route("/movies", methods=["POST"])
def add_movie():
    return add_movies(db)


@app.route("/movies", methods=["DELETE"])
def delete_movies():
    return delete_movie(db)


@app.route("/movies/find", methods=["GET"])
def find_movie():
    return find_movies(db)


@app.route("/vote/<int:id>", methods=["POST"])
def vote(id):
    return vote_main(id, db)


@app.route("/actors", methods=["GET"])
def actor():
    return actors(db)


@app.route("/actors", methods=["POST"])
def add_actor():
    return add_actors(db)


@app.route("/actors", methods=["DELETE"])
def del_actor():
    return del_actors(db)


@app.route("/actors/find")
def find_actor():
    return find_actors(db)


@app.route("/actors", methods=["PATCH"])
def edit_actors():
    return edit_actor(db)


if __name__ == '__main__':
    app.run(
        host=host,
        port=8001,
        debug=True
    )
