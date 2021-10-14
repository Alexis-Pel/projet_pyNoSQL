from assets.pageReturn import page_return
from assets.get_args import get_args


def movies(db):
    """
       Permet d'afficher une liste des films
       :return: type: json : Si Acteurs : Liste des films | Si non : 'No Movies' / Code html
       """
    collection = db["movies"]
    movie_list = []
    for movie in collection.find():
        movie_list.append(movie)
    if len(movie_list) == 0:
        return page_return('SUCCESS', 200, 'No Movies')
    else:
        return page_return('SUCCESS', 200, str(movie_list))


def add_movies(db):
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

    complete = True
    for arg in add_args:
        if arg is None or arg == "":
            complete = False

    if complete:
        collection.insert({
            "_id": int(add_args[0]),
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
    else:
        return page_return('ERROR', 400, 'Argument(s) incorrect')


def delete_movie(db):
    """
    Cette fonction permet de supprimer un film de la base de données
    :return: Une message de succès ou d'erreur
    """
    collection = db["movies"]
    args = get_args(["id"])

    show = collection.find_one({"_id": args[0]})

    if show is not None:
        collection.delete_one(show)
        return page_return('SUCCESS', 200, "Film supprimé")
    else:
        return page_return('ERROR', 404, 'Aucun film à cet Id')