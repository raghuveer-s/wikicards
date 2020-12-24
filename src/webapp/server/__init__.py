import os

from klein import Klein

from . import path


def create_app():
    app = Klein()

    @app.route("/")
    def hello():
        return "Hello World"

    @app.route("/article/<id>")
    def get_article(id):
        return "Article {}".format(id)
    
    @app.route("/search", methods = ['POST'])
    def search_path(first_url:str, second_url:str):
        return path.find_path(first_url, second_url)

    return app