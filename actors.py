from assets.pageReturn import page_return
from assets.get_args import get_args


def actors(db):
    """
    Permet d'afficher une liste des acteurs
    :return: type: json : Si Acteurs : Liste des acteurs | Si non : 'No Actors' / Code html
    """
    collection = db["actors"]
    actor_list = []
    for actor in collection.find():
        actor_list.append(actor)
    if len(actor_list) == 0:
        return page_return('SUCCESS', 200, 'No Actors')
    else:
        return page_return('SUCCESS', 200, str(actor_list))


def add_actors(db):
    """
    Cette fonction permet d'ajouter un actor dans la base de données
    :return: string: Message de succès ou erreur
    """
    collection = db["actors"]
    add_args = get_args(['id', 'name', 'age', 'genre'])
    complete = True
    for arg in add_args:
        if arg is None or arg == "":
            complete = False

    if complete:
        collection.insert({
            "_id": int(add_args[0]),
            "name": add_args[1],
            "age": add_args[2],
            "genre": add_args[3]
        })

    return page_return('SUCCESS', 200, 'Actors About')


def del_actors(db):
    """
    Cette fonction permet de supprimer un actor dans la base de données
    :return: string: Message de succès ou erreur
    """
    collection = db["actors"]
    del_args = get_args(['id', 'name', 'age', 'genre'])

    show = collection.find_one({"_id": int(del_args[0])})

    if show is not None:
        collection.delete_one(show)
        return page_return('SUCCESS', 200, "Actor Delete")
    else:
        return page_return('ERROR', 404, 'Aucun acteur à cet Id')


def edit_actor(db):
    collection = db['actors']
    actor_args = get_args(["name", "age", "genre", "id"])
    args = {}

    if actor_args[0] is None and actor_args[1] is None and actor_args[2] is None and actor_args[3] is None:
        return page_return('ERROR', 400, 'Aucun paramètre')

    for i in range(len(actor_args)):
        if actor_args[i] is not None:
            if not actor_args[i].isalnum():
                return page_return('ERROR', 400, 'Veuillez supprimer les caractères speciaux')
            if i == 0:
                if actor_args[i].isdigit():
                    return page_return('ERROR', 400, 'Erreur dans le paramètre NAME')
                else:
                    args['name'] = actor_args[i]
            elif i == 1:
                args['age'] = actor_args[i]
            elif i == 2:
                if actor_args[i].isdigit():
                    return page_return('ERROR', 400, 'Erreur dans le paramètre GENRE')
                elif actor_args[i] != "Homme" and actor_args[i] != "Femme" and actor_args[i] != "Non binaire":
                    return page_return('ERROR', 400, 'Genre : Homme, Femme, Non binaire')
                else:
                    args['genre'] = actor_args[i]
            elif i == 3:
                if not actor_args[i].isdigit():
                    return page_return('ERROR', 400, 'Erreur dans le paramètre ID')
        else:
            if actor_args[3] is None:
                return page_return('ERROR', 400, "Pas d'ID")

    actor = collection.find_one({'_id': actor_args[3]})
    if actor is None:
        return page_return("ERROR", 404, "Acteur Introuvable")
    else:
        collection.update_one(actor, {'$set': args})
        return page_return("SUCCESS", 200, "Acteur Modifié")