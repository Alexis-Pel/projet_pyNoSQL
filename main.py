from flask import Flask
from flask import request
from flask import make_response
from pymongo import mongo_client
import os

app = Flask(__name__)
host = os.environ["HOST"]


# username = os.environ["DB_USER"]
# password = os.environ["DB_PASS"]
# cluster = os.environ["CLUSTER"]
# database_name = os.environ["DB"]
# collection_name = os.environ["COLLECTION"]


def page_return(type, code, message):
    return make_response({"type": type, "code": code, "message": message}, code)


@app.route("/")
def home():
    return page_return('SUCCESS', 200, 'Accueil')


@app.route("/movies")
def movies():
    return page_return('SUCCESS', 200, 'Movies')


@app.route("/movies/find")
def find_movies():
    return page_return('SUCCESS', 200, 'Search Movies')


@app.route("/vote/id")
def vote():
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
