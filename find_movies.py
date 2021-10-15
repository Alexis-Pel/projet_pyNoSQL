import re

from assets.get_args import get_args
from assets.pageReturn import page_return


def find_movies(db):
    """
    Cette fonction permet de trouvé un film par rapport à ces params
    :return: Un message d'erreur ou de succès avec le film recherché
    """
    collections = db['movies']
    actors_collection = db['actors']
    search = {}
    movies = []

    movie_args = get_args(['title', 'category', 'release_date'])
    if movie_args[0] is None and movie_args[1] is None and movie_args[2] is None:
        return page_return('ERROR', 400, 'Aucun paramètre de recherche')

    if movie_args[0]:
        if movie_args[0].isdigit():
            return page_return('ERROR', 400, 'Erreur dans le paramètre TITLE')
        search['title'] = {'$regex': re.compile(movie_args[0], re.IGNORECASE)}

    if movie_args[1]:
        if not movie_args[1].isalnum() or movie_args[1].isdigit():
            return page_return('ERROR', 400, 'Erreur dans le paramètre CATEGORY')
        search['category'] = {'$regex': re.compile(movie_args[1], re.IGNORECASE)}

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
        return page_return('SUCCESS', 200, 'Aucun film trouvé')
    else:
        for movie in movies:
            actors_list = []
            for actor_id in movie['distribution']:
                actor_find = actors_collection.find_one({'_id':actor_id})
                actors_list.append(actor_find['name'])
            movie['distribution'] = actors_list
    return page_return('SUCCESS', 200, str(movies))
