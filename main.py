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
    """
    Cette fonction permet d'ajouter un film dans la base de données
    :return: string: Message de succès ou erreur
    """
    collection = db["movies"]
    add_args = ['id', 'title', 'category', 'synopsis', 'distribution', 'release_date', 'duration']
    add_args = get_args(add_args)
    distribution = add_args[4].split(',')
    likes = 0
    dislikes = 0

    collection.insert({
        "_id": add_args[0],
        "title": add_args[1],
        "category": add_args[2],
        "synopsis": add_args[3],
        "distribution": distribution,
        "release_date": add_args[5],
        "duration": add_args[6],
        "likes": likes,
        "dislikes": dislikes
    })
    return page_return('SUCCESS', 200, 'Film ajouté')



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


@app.route("/actors", methods=["GET"])
def actors():
    collection = db["actors"]
    actor_list = []
    for actor in collection.find():
        actor_list.append(actor)
    if len(actor_list) == 0:
        return page_return('SUCCESS', 200, 'No Actors')
    else:
        return page_return('SUCCESS', 200, str(actor_list))


@app.route("/actors", methods=["POST"])
def add_actors():
    id = request.args ['id']
    name = request.args['name']
    age = request.args['age']
    genre = request.args['genre']

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
