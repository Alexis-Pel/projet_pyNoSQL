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
collection_name = "movies"

client = MongoClient(f"mongodb+srv://{username}:{password}@{cluster}/{database_name}?retryWrites=true&w=majority")
db = client[database_name]
collection = db[collection_name]


def page_return(type, code, message):
    return make_response({"type": type, "code": code, "message": message}, code)


@app.route("/")
def home():
    return page_return('SUCCESS', 200, 'Accueil')


@app.route("/movies", methods=["GET"])
def movies():
    return page_return('SUCCESS', 200, 'Get_Movies')

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


@app.route("/actors", methods=["GET"])
def actors():
    return page_return('SUCCESS', 200, 'Actors')


@app.route("/actors", methods=["POST"])
def add_actors():
    id = request.args ['id']
    name = request.args['name']
    year = request.args['year']
    kind = request.args['kind']

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
