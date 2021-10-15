from flask import request


def get_args(args):
    """
    Cette fonction permet de recupérer les arguments
    :param args: Liste des arguments
    :return: Une liste d'arguments
    """
    args_return = []
    for arg in args:
        try:
            i = request.args[str(arg)]
        except:
            i = None
        args_return.append(i)
    return args_return
