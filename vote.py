from assets.pageReturn import page_return
from assets.get_args import get_args


def vote_main(id, db):
    """
    Permet d'ajouter un like / dislike à un film
    :param id: L'id du film qui reçoit le vote
    :return: type: json : Si film introuvable : 'film Introuvable' | Si pas de vote : 'Veuillez verifier le vote' |
    Si correct  : 'Vote effectué' / code html
    """
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
