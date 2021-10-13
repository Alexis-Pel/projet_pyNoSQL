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
    """
    Cette fonction permet d'ajouter un film dans la base de données
    :return: string: Message de succès ou erreur
    """
    collection = db["movies"]
    movies_id = request.args['id']
    title = request.args['title']
    category = request.args['category']
    synopsis = request.args['synopsis']
    distribution = request.args['distribution']
    distrib = distribution.split(', ')
    release_date = request.args['release_date']
    duration = request.args['duration']
    likes = 0
    dislikes = 0
    try:
        collection.insert({
            "_id": movies_id,
            "title": title,
            "category": category,
            "synopsis": synopsis,
            "distribution": distrib,
            "release_date": release_date,
            "duration": duration,
            "likes": likes,
            "dislikes": dislikes
        })
        return page_return('SUCCESS', 200, 'Film ajouté')
    except:
        return page_return('ERROR', 400, 'Bad Request - La syntaxe de la requête est erronée.')


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
