from flask import make_response


def page_return(type, code, message):
    return make_response({"type": type, "code": code, "message": message}, code)
