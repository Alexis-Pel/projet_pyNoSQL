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


def get_args(args):
    args_return = []
    for arg in args:
        try:
            i = request.args[str(arg)]
        except:
            i = None
        args_return.append(i)
    return args_return


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


@app.route("/vote/<int:id>", methods=["POST"])
def vote(id):
    global phrase
    collection = db["movies"]
    args = get_args(['like', 'dislike'])
    like, dislike = args[0], args[1]
    movie = collection.find_one({'_id': id})
    if movie is None:
        return page_return("ERROR", 404, "Film Introuvable")

    actual_likes = movie['likes']
    actual_dislikes = movie['dislikes']

    if like and dislike or like is None and dislike is None:
        return page_return("ERROR", 400, "Veuillez vérifier le vote")
    if like:
        phrase = {'likes': int(actual_likes) + 1}
    elif dislike:
        phrase = {'dislikes': int(actual_dislikes) + 1}

    collection.update_one(movie, {'$set': phrase})
    return page_return('SUCCESS', 200, 'Vote effectué')


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
