import re
from assets.pageReturn import page_return
from assets.get_args import get_args


def find_actors(db):
    """
    Cette fonction permet de chercher un actor dans la base de données
    :return: string: Message de succès ou erreur
    """
    collections = db['actors']
    search = {}
    actors = []

    actor_args = get_args(['name', 'age', 'genre'])
    if actor_args[0] is None and actor_args[1] is None and actor_args[2] is None:
        return page_return('ERROR', 400, 'Aucun paramètre de recherche')

    for i in range(len(actor_args)):
        if actor_args[i] is not None:
            if i == 0:
                if not actor_args[0].isalnum() or actor_args[0].isdigit():
                    return page_return('ERROR', 400, 'Erreur dans le paramètre NAME')
                else:
                    search['name'] = {'$regex': re.compile(actor_args[0], re.IGNORECASE)}

            elif i == 1:
                if not actor_args[1].isalnum():
                    return page_return('ERROR', 400, 'Erreur dans le paramètre AGE')
                else:
                    search['age'] = actor_args[1]

            elif i == 2:
                search['genre'] = actor_args[2]

    if not len(search) == 0:
        for actor in collections.find(search):
            actors.append(actor)
    else:
        return page_return('ERROR', 200, 'Verifiez paramètres')

    if len(actors) == 0:
        return page_return('SUCCESS', 200, 'Aucun acteur')
    else:
        return page_return('SUCCESS', 200, str(actors))
