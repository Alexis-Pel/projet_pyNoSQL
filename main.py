from flask import Flask
from flask import request
from flask import make_response
from pymongo import MongoClient
import os

app = Flask(__name__)
host = os.environ["HOST"]

username = os.environ["DB_USER"]
password = os.environ["DB_PASS"]
cluster = os.environ["CLUSTER"]
database_name = os.environ["DB"]
client = MongoClient(f"mongodb+srv://{username}:{password}@{cluster}/{database_name}?retryWrites=true&w=majority")
db = client[database_name]


def page_return(type, code, message):
    return make_response({"type": type, "code": code, "message": message}, code)


@app.route("/")
def home():
    return page_return('SUCCESS', 200, 'Accueil')


@app.route("/movies", methods=["GET"])
def movies():
    collection = db["movies"]
    movie_list = []
    for movie in collection.find():
        movie_list.append(movie)
    if len(movie_list) == 0:
        return page_return('SUCCESS', 200, 'No Movies')
    else:
        return page_return('SUCCESS', 200, str(movie_list))

@app.route("/movies", methods=["POST"])
def add_movies():
    movies_id = request.args['id']
    title = request.args['title']
    synopsis = request.args['synopsis']
    distribution = request.args['distribution']
    release_date = request.args['release_date']
    duration = request.args['duration']
    likes = 0
    dislikes = 0

@app.route("/movies/find")
def find_movies():
    return page_return('SUCCESS', 200, 'Search Movies')


@app.route("/vote/<int:id>")
def vote(id):
    return page_return('SUCCESS', 200, 'Vote')


@app.route("/actors")
def actors():
    return page_return('SUCCESS', 200, 'Actors')


@app.route("/actor/find")
def find_actors():
    return page_return('SUCCESS', 200, 'Search Actors')


if __name__ == '__main__':
    app.run(
        host=host,
        port=8001,
        debug=True
    )
