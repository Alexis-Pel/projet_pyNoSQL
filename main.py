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


@app.route("/")
def home():
    return page_return('SUCCESS', 200, 'Accueil')


def page_return(type, code, message):
    return make_response({"type": type, "code": code, "message": message}, code)


if __name__ == '__main__':
    app.run(
        host=host,
        port=8001,
        debug=True
    )
