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
    collection.insert_one(
        {'_id': 0, 'title': 'Deadpool', 'category': 'Super-Hero', 'synopsis': "Deadpool, est l'anti-héros le plus atypique de l'univers Marvel. A l'origine, il s'appelle Wade Wilson : un ancien militaire des Forces Spéciales devenu mercenaire. Après avoir subi une expérimentation hors norme qui va accélérer ses pouvoirs de guérison, il va devenir Deadpool. Armé de ses nouvelles capacités et d'un humour noir survolté, Deadpool va traquer l'homme qui a bien failli anéantir sa vie.", 'distribution': ['Ryan Reynolds',
                                                                                                   'Morena Baccarin'],
         'release_date': '2016', 'duration': '108','likes': 1028, 'dislikes': 256})

    return page_return('SUCCESS', 200, 'Accueil')


@app.route("/movies", methods=["GET"])
def movies():
    return page_return('SUCCESS', 200, 'Get_Movies')


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
