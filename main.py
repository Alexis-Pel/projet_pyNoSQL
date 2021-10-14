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


@app.route("/movies", methods=["DELETE"])
def delete_movie():
    """
    Cette fonction permet de supprimer un film de la base de données
    :return: Une message de succès ou d'erreur
    """
    collection = db["movies"]
    args = get_args(["id"])

    movie_to_delete = {"_id": args[0]}
    show = collection.find_one(movie_to_delete)

    if show is not None:
        collection.delete_one(movie_to_delete)
        return page_return('SUCCESS', 200, "Film supprimé")
    else:
        return page_return('ERROR', 404, 'Aucun film à cet Id')


@app.route("/movies/find", methods=["GET"])
def find_movies():
    """
    Cette fonction permet de trouvé un film par rapport à ces params
    :return: Un message d'erreur ou de succès avec le film recherché
    """
    collections = db['movies']
    search = {}
    movies = []

    movie_args = get_args(['title', 'category', 'release_date'])
    if movie_args[0] is None and movie_args[1] is None and movie_args[2] is None:
        return page_return('ERROR', 400, 'Aucun paramètre de recherche')

    if movie_args[0]:
        if movie_args[0].isdigit():
            return page_return('ERROR', 400, 'Erreur dans le paramètre TITLE')
        search['title'] = {'$regex': movie_args[0]}

    if movie_args[1]:
        if not movie_args[1].isalnum() or movie_args[1].isdigit():
            return page_return('ERROR', 400, 'Erreur dans le paramètre CATEGORY')
        search['category'] = {'$regex': movie_args[1]}

    if movie_args[2]:
        if not movie_args[2].isalnum() or not movie_args[2].isdigit():
            return page_return('ERROR', 400, 'Erreur dans le paramètre RELEASE_DATE')
        search['release_date'] = movie_args[2]
    if not len(search) == 0:
        for movie in collections.find(search):
            movies.append(movie)
    else:
        return page_return('ERROR', 200, 'Verifiez paramètres')
    if len(movies) == 0:
        return page_return('SUCCESS', 200, 'Aucun acteur')

    return page_return('SUCCESS', 200, str(movies))


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
    collection = db["actors"]
    add_args = ['id', 'name', 'age', 'genre']
    add_args = get_args(add_args)

    collection.insert({
        "_id": add_args[0],
        "name": add_args[1],
        "age": add_args[2],
        "genre": add_args[3]
    })

    return page_return('SUCCESS', 200, 'Actors About')


@app.route("/actors", methods=["DELETE"])
def del_actors():
    collection = db["actors"]
    add_args = ['id', 'name', 'age', 'genre']
    add_args = get_args(add_args)

    collection.delete_one({
        "_id": add_args[0],
        "name": add_args[1],
        "age": add_args[2],
        "genre": add_args[3]
    })

    return page_return('SUCCESS', 200, 'Actors Delete')


@app.route("/actors/find")
def find_actors():
    collections = db['actors']
    search = {}
    actors = []

    actor_args = get_args(['name', 'age', 'genre'])
    if actor_args[0] is None and actor_args[1] is None and actor_args[2] is None:
        return page_return('ERROR', 400, 'Aucun paramètre de recherche')

    if actor_args[0]:
        if not actor_args[0].isalnum() or actor_args[0].isdigit():
            return page_return('ERROR', 400, 'Erreur dans le paramètre NAME')
        search['name'] = {'$regex': actor_args[0]}

    if actor_args[1]:
        if not actor_args[1].isalnum():
            return page_return('ERROR', 400, 'Erreur dans le paramètre AGE')
        search['age'] = int(actor_args[1])

    if actor_args[2]:
        search['genre'] = actor_args[2]
    if not len(search) == 0:
        for actor in collections.find(search):
            actors.append(actor)
    else:
        return page_return('ERROR', 200, 'Verifiez paramètres')
    if len(actors) == 0:
        return page_return('SUCCESS', 200, 'Aucun acteur')

    return page_return('SUCCESS', 200, str(actors))


if __name__ == '__main__':
    app.run(
        host=host,
        port=8001,
        debug=True
    )
