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
    add_args = get_args(['id', 'title', 'category', 'synopsis', 'distribution', 'release_date', 'duration'])

    for arg in add_args:
        if (arg is None or arg == "") and arg.isdigit():
            return page_return('ERROR', 400, 'Argument(s) incorrect')

    collection.insert({
        "_id": int(add_args[0]),
        "title": add_args[1],
        "category": add_args[2],
        "synopsis": add_args[3],
        "distribution": add_args[4].split(','),
        "release_date": add_args[5],
        "duration": add_args[6],
        "likes": 0,
        "dislikes": 0
    })
    return page_return('SUCCESS', 200, 'Film ajouté')


def delete_movie(db):
    """
    Cette fonction permet de supprimer un film de la base de données
    :return: Une message de succès ou d'erreur
    """
    collection = db["movies"]
    args = get_args(["id"])

    show = collection.find_one({"_id": int(args[0])})

    if show is not None:
        collection.delete_one(show)
        return page_return('SUCCESS', 200, "Film supprimé")
    else:
        return page_return('ERROR', 404, 'Aucun film à cet Id')


def edit_movie(db):
    """
    Cette fonction permet de modifier un film dans la base de données
    :return: :return: string: Message de succès ou erreur
    """
    collection = db['movies']
    movie_args = get_args(["title", "category", "synopsis", "distribution", "release_date", "duration", "id"])
    args = {}
    nones = 0

    for i in range(len(movie_args)):
        if movie_args[i] is not None:
            if not movie_args[i].isalnum():
                return page_return('ERROR', 400, 'Veuillez supprimer les carctères spéciaux')
            if i == 0:
                if movie_args[i].isdigit():
                    return page_return('ERROR', 400, 'Erreur dans le paramètre Title')
                else:
                    args['title'] = movie_args[i]

            elif i == 1:
                if movie_args[i].isdigit():
                    return page_return('ERROR', 400, 'Erreur dans le paramètre Category')
                else:
                    args['category'] = movie_args[i]

            elif i == 2:
                if movie_args[i].isdigit():
                    return page_return('ERROR', 400, 'Erreur dans le paramètre Synopsis')
                else:
                    args['synopsis'] = movie_args[i]

            elif i == 3:
                if movie_args[i].isdigit():
                    return page_return('ERROR', 400, 'Erreur dans le paramètre Distibution')
                else:
                    args['distribution'] = movie_args[i]

            elif i == 4:
                if movie_args[i].isdigit():
                    args['release_date'] = movie_args[i]
                else:
                    return page_return('ERROR', 400, 'Erreur dans le paramètre release_date')

            elif i == 5:
                if movie_args[i].isdigit():
                    args['duration'] = movie_args[i]
                else:
                    return page_return('ERROR', 400, 'Erreur dans le paramètre duration')
            elif i == 6:
                if not movie_args[i].isdigit():
                    return page_return('ERROR', 400, 'Erreur dans le paramètre ID')
        else:
            nones += 1
            if nones == len(movie_args):
                return page_return('ERROR', 400, 'Aucun paramètre de recherche')
            if movie_args[5] is None:
                return page_return('ERROR', 400, "Pas d'ID")

    movie = collection.find_one({'_id': int(movie_args[6])})

    if movie is None:
        return page_return("ERROR", 404, "Film introuvable")
    else:
        collection.update_one(movie, {'$set': args})
        return page_return("SUCCESS", 200, "Film modifié")
