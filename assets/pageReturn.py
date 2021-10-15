from flask import make_response


def page_return(type, code, message):
    """
    Cette fonction permet d'afficher la page de réponse avec le code statut correspondant
    :param type: Error ou Success
    :param code: Le code de l'erreur
    :param message: Le message d'erreur ou de succès à afficher
    :return: La réponse créée qui est un objet
    """
    return make_response({"type": type, "code": code, "message": message}, code)
